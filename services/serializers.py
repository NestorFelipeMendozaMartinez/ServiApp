from rest_framework import serializers
from .models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']


class ServiceSerializer(serializers.ModelSerializer):
    provider_username = serializers.ReadOnlyField(source='provider.username')
    provider_id = serializers.ReadOnlyField(source='provider.id')
    provider_rating = serializers.ReadOnlyField(source='provider.profile.rating')
    category_name = serializers.ReadOnlyField(source='category.name')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'provider_id', 'provider_username', 'provider_rating',
            'category', 'category_name', 'title', 'description',
            'price', 'city', 'image', 'image_url', 'is_active', 'created_at',
        ]
        read_only_fields = ['provider', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
