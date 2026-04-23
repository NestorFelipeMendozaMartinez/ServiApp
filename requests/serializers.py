from rest_framework import serializers
from .models import ServiceRequest, Offer, Review, Transaction
from services.serializers import ServiceCategorySerializer
from users.serializers import UserSerializer

class ServiceRequestSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ServiceRequest
        fields = ['id', 'client', 'category', 'category_id', 'title', 'description', 'latitude', 'longitude', 'status', 'created_at']

class OfferSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)
    request = ServiceRequestSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'request', 'provider', 'price', 'message', 'status', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed = UserSerializer(read_only=True)
    request = ServiceRequestSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed', 'request', 'rating', 'comment', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    request = ServiceRequestSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'request', 'amount', 'payment_method', 'status', 'created_at']