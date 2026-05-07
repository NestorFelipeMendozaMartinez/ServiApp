from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny

from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ServiceListView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related('provider', 'category')

        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        city = self.request.query_params.get('city')
        provider = self.request.query_params.get('provider')

        if category:
            queryset = queryset.filter(category_id=category)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if provider:
            queryset = queryset.filter(provider_id=provider)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(provider__username__icontains=search)
            )

        return queryset.order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Debes iniciar sesión para publicar un servicio.')
        serializer.save(provider=self.request.user)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Debes iniciar sesión.')
        service = self.get_object()
        if self.request.user != service.provider:
            raise PermissionDenied('No autorizado')
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('Debes iniciar sesión.')
        if self.request.user != instance.provider:
            raise PermissionDenied('No autorizado')
        instance.delete()
