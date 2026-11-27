from rest_framework import serializers
from apps.listings.models import Listing, ListingImage
from apps.categories.serializers import CategorySerializer
from apps.accounts.serializers.user_serializer import UserSerializer

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'url', 'position']

class ListingListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.CharField(source='primary_image_url', read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    formatted_old_price = serializers.CharField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'price', 'formatted_price', 'old_price', 'formatted_old_price',
            'is_promotion', 'promotion_text', 'city', 'category', 'primary_image',
            'status', 'views_count', 'created_at'
        ]

class ListingDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    formatted_old_price = serializers.CharField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'formatted_price',
            'old_price', 'formatted_old_price', 'category',
            'lat', 'lng', 'city', 'address', 'status',
            'views_count', 'user', 'images', 'created_at'
        ]

class ListingCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'category_id',
            'lat', 'lng', 'city', 'address'
        ]

class MapListingSerializer(serializers.ModelSerializer):
    primary_image = serializers.CharField(source='primary_image_url', read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'price', 'lat', 'lng', 'city', 'primary_image']
