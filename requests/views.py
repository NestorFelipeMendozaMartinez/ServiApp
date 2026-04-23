from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ServiceRequest, Offer, Review, Transaction
from .serializers import ServiceRequestSerializer, OfferSerializer, ReviewSerializer, TransactionSerializer

class ServiceRequestListView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceRequest.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request_id = self.request.query_params.get('request')
        if request_id:
            return Offer.objects.filter(request_id=request_id)
        return Offer.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(request__client=self.request.user) | Transaction.objects.filter(request__offers__provider=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save()
