from django.urls import path
from apps.listings.controllers.api.listings import (
    ListingListCreateAPIView,
    ListingDetailAPIView,
    ListingMapAPIView,
    ListingImageUploadAPIView
)

urlpatterns = [
    path('', ListingListCreateAPIView.as_view(), name='api_listings_list_create'),
    path('<int:pk>', ListingDetailAPIView.as_view(), name='api_listings_detail'),
    path('map', ListingMapAPIView.as_view(), name='api_listings_map'),
    path('map/', ListingMapAPIView.as_view()),
    path('<int:pk>/images', ListingImageUploadAPIView.as_view(), name='api_listings_images'),
]
