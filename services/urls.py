from django.urls import path
from .views import CategoryListView, ServiceListView, ServiceDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', ServiceListView.as_view()),
    path('<int:pk>/', ServiceDetailView.as_view()),
]