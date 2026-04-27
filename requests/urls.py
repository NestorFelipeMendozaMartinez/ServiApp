from django.urls import path
from .views import ServiceRequestListView, ServiceRequestDetailView, OfferListView, OfferDetailView, ReviewListView, TransactionListView, OfferContractView, OfferContractSignView

urlpatterns = [
    path('requests/', ServiceRequestListView.as_view(), name='requests'),
    path('requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='request-detail'),
    path('offers/', OfferListView.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offers/<int:pk>/contract/', OfferContractView.as_view(), name='offer-contract'),
    path('offers/<int:pk>/contract-sign/', OfferContractSignView.as_view(), name='offer-contract-sign'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
]