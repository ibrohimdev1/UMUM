from rest_framework import serializers
from apps.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'phone', 'email', 'full_name', 'role',
            'status', 'city', 'seller_profile_completed',
            'avatar', 'created_at'
        ]
        read_only_fields = ['id', 'role', 'status', 'created_at']

class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True)
    code = serializers.CharField(max_length=6, required=True)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'city', 'avatar']

class SellerProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150, required=True)
    city = serializers.CharField(max_length=100, required=True)
