from rest_framework import serializers
from .models import ServiceRequest, Offer, Review, Transaction, Contract, Message, Notification


class ServiceRequestSerializer(serializers.ModelSerializer):
    client_username = serializers.ReadOnlyField(source='client.username')
    client_id = serializers.ReadOnlyField(source='client.id')
    category_name = serializers.ReadOnlyField(source='category.name')
    offers_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'client', 'client_id', 'client_username', 'category', 'category_name',
            'title', 'description', 'location', 'city', 'image', 'image_url',
            'latitude', 'longitude', 'status', 'created_at', 'offers_count',
        ]
        read_only_fields = ['client', 'created_at']

    def get_offers_count(self, obj):
        return obj.offers.count()

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class OfferSerializer(serializers.ModelSerializer):
    provider_username = serializers.ReadOnlyField(source='provider.username')
    provider_id = serializers.ReadOnlyField(source='provider.id')
    provider_rating = serializers.ReadOnlyField(source='provider.profile.rating')
    provider_city = serializers.ReadOnlyField(source='provider.profile.city')
    request_title = serializers.ReadOnlyField(source='request.title')
    request_status = serializers.ReadOnlyField(source='request.status')

    class Meta:
        model = Offer
        fields = [
            'id', 'request', 'request_title', 'request_status',
            'provider', 'provider_id', 'provider_username', 'provider_rating', 'provider_city',
            'price', 'message', 'status', 'created_at',
        ]
        read_only_fields = ['provider', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')
    reviewed_username = serializers.ReadOnlyField(source='reviewed.username')

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewer_username', 'reviewed', 'reviewed_username',
            'request', 'rating', 'comment', 'created_at',
        ]
        read_only_fields = ['reviewer', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    sender_id = serializers.ReadOnlyField(source='sender.id')

    class Meta:
        model = Message
        fields = ['id', 'service_request', 'sender', 'sender_id', 'sender_username', 'content', 'read', 'created_at']
        read_only_fields = ['sender', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'body', 'read', 'link', 'created_at']
        read_only_fields = ['created_at']
