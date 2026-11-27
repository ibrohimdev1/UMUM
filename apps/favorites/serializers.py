from rest_framework import serializers
from apps.favorites.models import Favorite
from apps.listings.serializers import ListingListSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    listing = ListingListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'listing', 'created_at']
