from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ServiceCategory, Service
from .serializers import ServiceCategorySerializer, ServiceSerializer

class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceListView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Service.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
