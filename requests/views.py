from io import BytesIO
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ServiceRequest, Offer, Review, Transaction, Contract, Message, Notification
from .serializers import (
    ServiceRequestSerializer, OfferSerializer, ReviewSerializer,
    TransactionSerializer, ContractSerializer, MessageSerializer, NotificationSerializer,
)


def create_notification(user, ntype, title, body='', link=''):
    Notification.objects.create(user=user, type=ntype, title=title, body=body, link=link)


class ServiceRequestListView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        status_param = self.request.query_params.get('status')
        city = self.request.query_params.get('city')

        if self.request.user.profile.is_provider:
            queryset = ServiceRequest.objects.filter(Q(status='open') | Q(client=self.request.user))
        else:
            queryset = ServiceRequest.objects.filter(client=self.request.user)

        if category:
            queryset = queryset.filter(category_id=category)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset.distinct().order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.request.user.profile.is_provider:
            return ServiceRequest.objects.filter(Q(status='open') | Q(client=self.request.user))
        return ServiceRequest.objects.filter(client=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        request_obj = self.get_object()
        if self.request.user != request_obj.client and not self.request.user.is_staff:
            raise PermissionDenied('No autorizado para modificar esta solicitud.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.client and not self.request.user.is_staff:
            raise PermissionDenied('No autorizado para eliminar esta solicitud.')
        instance.delete()


class RequestCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        if request.user != service_request.client:
            return Response({'detail': 'Solo el cliente puede marcar como completada.'}, status=status.HTTP_403_FORBIDDEN)
        if service_request.status != 'in_progress':
            return Response({'detail': 'La solicitud debe estar en progreso.'}, status=status.HTTP_400_BAD_REQUEST)

        service_request.status = 'completed'
        service_request.save()

        accepted_offer = Offer.objects.filter(request=service_request, status='accepted').first()
        if accepted_offer:
            create_notification(
                accepted_offer.provider, 'request_completed',
                f'Solicitud completada: {service_request.title}',
                'El cliente marcó la solicitud como completada.',
                f'/requests/{service_request.id}',
            )

        return Response({'status': 'completed'})


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request_id = self.request.query_params.get('request')
        if request_id:
            service_request = get_object_or_404(ServiceRequest, id=request_id)
            if self.request.user == service_request.client:
                return Offer.objects.filter(request=service_request)
            return Offer.objects.filter(request=service_request, provider=self.request.user)

        if self.request.user.profile.is_provider:
            return Offer.objects.filter(provider=self.request.user).order_by('-created_at')
        return Offer.objects.filter(request__client=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        if not self.request.user.profile.is_provider:
            raise PermissionDenied('Solo los proveedores pueden enviar ofertas.')

        request_id = self.request.data.get('request_id') or self.request.data.get('request')
        service_request = get_object_or_404(ServiceRequest, id=request_id)

        if service_request.client == self.request.user:
            raise PermissionDenied('No puedes ofertar tu propia solicitud.')
        if service_request.status != 'open':
            raise ValidationError('La solicitud no está abierta para ofertas.')

        if Offer.objects.filter(request=service_request, provider=self.request.user).exists():
            raise ValidationError('Ya enviaste una oferta para esta solicitud.')

        offer = serializer.save(provider=self.request.user, request=service_request)

        create_notification(
            service_request.client, 'new_offer',
            f'Nueva oferta para: {service_request.title}',
            f'{self.request.user.username} envió una oferta de ${offer.price}',
            f'/requests/{service_request.id}',
        )


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.profile.is_provider:
            return Offer.objects.filter(Q(provider=self.request.user) | Q(request__client=self.request.user))
        return Offer.objects.filter(request__client=self.request.user)

    def perform_update(self, serializer):
        offer = self.get_object()
        status_value = self.request.data.get('status')

        if status_value == 'accepted':
            if self.request.user != offer.request.client and not self.request.user.is_staff:
                raise PermissionDenied('Solo el cliente puede aceptar esta oferta.')
            offer.request.status = 'in_progress'
            offer.request.save()
            Offer.objects.filter(request=offer.request).exclude(pk=offer.pk).update(status='rejected')
            create_notification(
                offer.provider, 'offer_accepted',
                f'¡Tu oferta fue aceptada!',
                f'El cliente aceptó tu oferta para: {offer.request.title}',
                f'/requests/{offer.request.id}',
            )

        if status_value == 'rejected':
            if self.request.user != offer.request.client and self.request.user != offer.provider and not self.request.user.is_staff:
                raise PermissionDenied('No autorizado para rechazar esta oferta.')
            create_notification(
                offer.provider, 'offer_rejected',
                'Tu oferta fue rechazada',
                f'El cliente rechazó tu oferta para: {offer.request.title}',
                f'/requests/{offer.request.id}',
            )

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.provider and self.request.user != instance.request.client and not self.request.user.is_staff:
            raise PermissionDenied('No autorizado para eliminar esta oferta.')
        instance.delete()


class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        received = self.request.query_params.get('received')
        provider_id = self.request.query_params.get('provider')
        if provider_id:
            return Review.objects.filter(reviewed_id=provider_id).order_by('-created_at')
        if received == 'true':
            return Review.objects.filter(reviewed=self.request.user)
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        request_id = self.request.data.get('request_id') or self.request.data.get('request')
        reviewed_id = self.request.data.get('reviewed_id') or self.request.data.get('reviewed')
        service_request = get_object_or_404(ServiceRequest, pk=request_id)
        reviewed_user = get_object_or_404(User, pk=reviewed_id)

        if self.request.user != service_request.client:
            raise PermissionDenied('Solo el cliente puede dejar una reseña.')
        if service_request.status != 'completed':
            raise ValidationError('Solo se puede calificar solicitudes completadas.')
        if Review.objects.filter(reviewer=self.request.user, request=service_request).exists():
            raise ValidationError('Ya dejaste una reseña para esta solicitud.')

        accepted_offer = Offer.objects.filter(request=service_request, status='accepted').first()
        if not accepted_offer or accepted_offer.provider != reviewed_user:
            raise ValidationError('Solo se puede calificar al proveedor de la oferta aceptada.')

        review = serializer.save(reviewer=self.request.user, reviewed=reviewed_user, request=service_request)
        self._update_provider_rating(reviewed_user)
        create_notification(
            reviewed_user, 'new_review',
            '¡Tienes una nueva reseña!',
            f'{self.request.user.username} te dejó {review.rating} estrellas.',
            f'/providers/{reviewed_user.id}',
        )

    def _update_provider_rating(self, provider):
        result = Review.objects.filter(reviewed=provider).aggregate(avg_rating=Avg('rating'))
        provider.profile.rating = result['avg_rating'] or 0.0
        provider.profile.total_ratings = Review.objects.filter(reviewed=provider).count()
        provider.profile.save()


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Transaction.objects.filter(request__client=self.request.user) |
            Transaction.objects.filter(request__offers__provider=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        request_id = self.request.data.get('request_id') or self.request.data.get('request')
        service_request = get_object_or_404(ServiceRequest, pk=request_id, client=self.request.user)
        serializer.save(request=service_request)


class OfferContractSignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        if request.user != offer.provider and request.user != offer.request.client:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        contract, _ = Contract.objects.get_or_create(offer=offer)
        signature = request.data.get('signature') or request.user.get_full_name() or request.user.username

        if request.user == offer.provider:
            contract.provider_signed = True
            contract.provider_signature = signature
        else:
            contract.client_signed = True
            contract.client_signature = signature

        contract.save()
        return Response(ContractSerializer(contract).data)


class OfferContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        if request.user != offer.provider and request.user != offer.request.client:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        contract, _ = Contract.objects.get_or_create(offer=offer)
        pdf_buffer = _generate_contract_pdf(offer, contract)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contrato_oferta_{offer.id}.pdf"'
        return response


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request_id = self.request.query_params.get('request')
        if not request_id:
            return Message.objects.none()
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        if self.request.user != service_request.client:
            accepted_offer = Offer.objects.filter(request=service_request, status='accepted', provider=self.request.user).first()
            if not accepted_offer:
                raise PermissionDenied('No tienes acceso a este chat.')
        Message.objects.filter(service_request=service_request).exclude(sender=self.request.user).update(read=True)
        return Message.objects.filter(service_request=service_request)

    def perform_create(self, serializer):
        request_id = self.request.data.get('service_request') or self.request.data.get('request_id')
        service_request = get_object_or_404(ServiceRequest, id=request_id)

        if self.request.user != service_request.client:
            accepted_offer = Offer.objects.filter(request=service_request, status='accepted', provider=self.request.user).first()
            if not accepted_offer:
                raise PermissionDenied('No tienes acceso a este chat.')

        msg = serializer.save(sender=self.request.user, service_request=service_request)

        recipient = service_request.client if self.request.user != service_request.client else None
        if not recipient:
            accepted_offer = Offer.objects.filter(request=service_request, status='accepted').first()
            if accepted_offer:
                recipient = accepted_offer.provider

        if recipient:
            create_notification(
                recipient, 'new_message',
                f'Nuevo mensaje de {self.request.user.username}',
                msg.content[:100],
                f'/requests/{service_request.id}',
            )


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return Response({'status': 'ok'})


def _generate_contract_pdf(offer, contract):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, 750, 'Contrato de Servicio - ServiApp')
    pdf.setFont('Helvetica', 11)
    pdf.drawString(50, 730, f'Oferta ID: {offer.id}')
    pdf.drawString(50, 715, f'Servicio: {offer.request.title}')
    pdf.drawString(50, 700, f'Categoría: {offer.request.category.name}')
    pdf.drawString(50, 685, f'Descripción: {offer.request.description[:80]}')
    pdf.drawString(50, 670, f'Proveedor: {offer.provider.get_full_name() or offer.provider.username}')
    pdf.drawString(50, 655, f'Cliente: {offer.request.client.get_full_name() or offer.request.client.username}')
    pdf.drawString(50, 640, f'Ubicación: {offer.request.location or "No especificada"}')
    pdf.drawString(50, 625, f'Precio acordado: ${offer.price}')
    pdf.drawString(50, 605, 'Garantías:')
    text = pdf.beginText(50, 590)
    text.textLines([
        '- El proveedor se compromete a prestar el servicio con diligencia y calidad.',
        '- El cliente se compromete a pagar el precio acordado al finalizar.',
        '- Ambas partes reconocen este contrato como compromiso válido.',
    ])
    pdf.drawText(text)
    pdf.drawString(50, 540, f'Cliente firmado: {"Sí" if contract.client_signed else "No"}')
    pdf.drawString(50, 525, f'Proveedor firmado: {"Sí" if contract.provider_signed else "No"}')
    pdf.drawString(50, 510, f'Firma cliente: {contract.client_signature or "Pendiente"}')
    pdf.drawString(50, 495, f'Firma proveedor: {contract.provider_signature or "Pendiente"}')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
