from io import BytesIO
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ServiceRequest, Offer, Review, Transaction, Contract
from .serializers import ServiceRequestSerializer, OfferSerializer, ReviewSerializer, TransactionSerializer, ContractSerializer

class ServiceRequestListView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        status_param = self.request.query_params.get('status')

        if self.request.user.profile.is_provider:
            queryset = ServiceRequest.objects.filter(Q(status='open') | Q(client=self.request.user))
        else:
            queryset = ServiceRequest.objects.filter(client=self.request.user)

        if category:
            queryset = queryset.filter(category_id=category)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset.distinct().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.profile.is_provider:
            return ServiceRequest.objects.filter(Q(status='open') | Q(client=self.request.user))
        return ServiceRequest.objects.filter(client=self.request.user)

    def perform_update(self, serializer):
        request_obj = self.get_object()
        if self.request.user != request_obj.client and not self.request.user.is_staff:
            raise PermissionDenied('No autorizado para modificar esta solicitud.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.client and not self.request.user.is_staff:
            raise PermissionDenied('No autorizado para eliminar esta solicitud.')
        instance.delete()

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
            return Offer.objects.filter(provider=self.request.user)
        return Offer.objects.filter(request__client=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.profile.is_provider:
            raise PermissionDenied('Solo los proveedores pueden enviar ofertas.')

        request_id = self.request.data.get('request_id')
        service_request = get_object_or_404(ServiceRequest, id=request_id)

        if service_request.client == self.request.user:
            raise PermissionDenied('No puedes ofertar tu propia solicitud.')
        if service_request.status != 'open':
            raise ValidationError('La solicitud no está abierta para ofertas.')

        serializer.save(provider=self.request.user, request=service_request)

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

        if status_value == 'rejected':
            if self.request.user != offer.request.client and self.request.user != offer.provider and not self.request.user.is_staff:
                raise PermissionDenied('No autorizado para rechazar esta oferta.')

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
        if received == 'true':
            return Review.objects.filter(reviewed=self.request.user)
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        request_id = self.request.data.get('request_id')
        reviewed_id = self.request.data.get('reviewed_id')
        service_request = get_object_or_404(ServiceRequest, pk=request_id)
        reviewed_user = get_object_or_404(User, pk=reviewed_id)

        if self.request.user != service_request.client:
            raise PermissionDenied('Solo el cliente puede dejar una reseña.')
        if service_request.status != 'completed':
            raise ValidationError('Solo se puede calificar solicitudes completadas.')

        accepted_offer = Offer.objects.filter(request=service_request, status='accepted').first()
        if not accepted_offer or accepted_offer.provider != reviewed_user:
            raise ValidationError('Solo se puede calificar al proveedor de la oferta aceptada.')

        review = serializer.save(reviewer=self.request.user, reviewed=reviewed_user, request=service_request)
        self.update_provider_rating(reviewed_user)

    def update_provider_rating(self, provider):
        result = Review.objects.filter(reviewed=provider).aggregate(avg_rating=Avg('rating'))
        reviews = Review.objects.filter(reviewed=provider)
        provider.profile.rating = result['avg_rating'] or 0.0
        provider.profile.total_ratings = reviews.count()
        provider.profile.save()

class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(request__client=self.request.user) | Transaction.objects.filter(request__offers__provider=self.request.user).distinct()

    def perform_create(self, serializer):
        request_id = self.request.data.get('request_id')
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
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

class OfferContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        if request.user != offer.provider and request.user != offer.request.client:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        contract, _ = Contract.objects.get_or_create(offer=offer)
        pdf_buffer = generate_contract_pdf(offer, contract)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contract_offer_{offer.id}.pdf"'
        return response


def generate_contract_pdf(offer, contract):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, 750, 'Contrato de Servicio')
    pdf.setFont('Helvetica', 11)
    pdf.drawString(50, 730, f'Oferta ID: {offer.id}')
    pdf.drawString(50, 715, f'Servicio: {offer.request.title}')
    pdf.drawString(50, 700, f'Categoría: {offer.request.category.name}')
    pdf.drawString(50, 685, f'Descripción del servicio: {offer.request.description}')
    pdf.drawString(50, 670, f'Proveedor: {offer.provider.get_full_name() or offer.provider.username}')
    pdf.drawString(50, 655, f'Cliente: {offer.request.client.get_full_name() or offer.request.client.username}')
    pdf.drawString(50, 640, f'Ubicación del cliente: {offer.request.location or "No especificada"}')
    pdf.drawString(50, 625, f'Precio acordado: ${offer.price}')
    pdf.drawString(50, 610, 'Garantías:')
    text = pdf.beginText(50, 595)
    text.textLines([
        'El proveedor se compromete a prestar el servicio con diligencia y calidad.',
        'El cliente acepta que el proveedor realice las tareas acordadas y pague al finalizar.',
        'Ambas partes reconocen este contrato como compromiso válido y aceptan sus condiciones.',
    ])
    pdf.drawText(text)

    pdf.drawString(50, 545, f'Cliente firmado: {"Sí" if contract.client_signed else "No"}')
    pdf.drawString(50, 525, f'Proveedor firmado: {"Sí" if contract.provider_signed else "No"}')
    pdf.drawString(50, 505, f'Firma cliente: {contract.client_signature or "Pendiente"}')
    pdf.drawString(50, 485, f'Firma proveedor: {contract.provider_signature or "Pendiente"}')
    pdf.drawString(50, 455, 'Fecha de emisión: ________________________________________')
    pdf.drawString(50, 430, 'Firma digital cliente: ____________________________________')
    pdf.drawString(50, 405, 'Firma digital proveedor: _________________________________')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
