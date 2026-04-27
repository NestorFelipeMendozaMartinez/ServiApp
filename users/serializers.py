from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'phone', 'location', 'bio', 'is_provider', 'role', 'rating', 'total_ratings']

    def get_role(self, obj):
        if obj.user.is_superuser or obj.user.is_staff:
            return 'Administrador'
        return 'Proveedor' if obj.is_provider else 'Cliente'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user