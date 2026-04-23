from django.urls import path
from .views import ServiceCategoryListView, ServiceListView, ServiceDetailView

urlpatterns = [
    path('categories/', ServiceCategoryListView.as_view(), name='categories'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]