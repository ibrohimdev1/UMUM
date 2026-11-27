from django.urls import path
from apps.listings.controllers.web.listings import (
    ListingListView,
    ListingDetailView,
    ListingCreateView,
    MyListingsView,
    MapView
)

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('create/', ListingCreateView.as_view(), name='listing_create'),
    path('my/', MyListingsView.as_view(), name='my_listings'),
    path('map/', MapView.as_view(), name='map_view'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
]
