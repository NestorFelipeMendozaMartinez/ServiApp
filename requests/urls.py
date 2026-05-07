from django.urls import path
from .views import (
    ServiceRequestListView, ServiceRequestDetailView, RequestCompleteView,
    OfferListView, OfferDetailView, OfferContractView, OfferContractSignView,
    ReviewListView, TransactionListView,
    MessageListView, NotificationListView, NotificationMarkReadView,
)

urlpatterns = [
    path('requests/', ServiceRequestListView.as_view(), name='requests'),
    path('requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:pk>/complete/', RequestCompleteView.as_view(), name='request-complete'),
    path('offers/', OfferListView.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offers/<int:pk>/contract/', OfferContractView.as_view(), name='offer-contract'),
    path('offers/<int:pk>/contract-sign/', OfferContractSignView.as_view(), name='offer-contract-sign'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/read/', NotificationMarkReadView.as_view(), name='notifications-read'),
]
