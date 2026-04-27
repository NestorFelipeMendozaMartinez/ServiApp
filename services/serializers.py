from rest_framework import serializers
from .models import ServiceCategory, Service
from users.serializers import UserSerializer

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)
    provider_rating = serializers.FloatField(source='provider.profile.rating', read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Service
        fields = ['id', 'provider', 'provider_rating', 'category', 'category_id', 'title', 'description', 'price', 'created_at']