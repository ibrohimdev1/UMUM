from rest_framework import serializers
from apps.orders.models import Order
from apps.listings.serializers import ListingListSerializer
from apps.accounts.serializers.user_serializer import UserSerializer

class OrderSerializer(serializers.ModelSerializer):
    listing = ListingListSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'listing', 'buyer', 'amount', 'status', 'created_at']

class OrderCreateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(required=True)
