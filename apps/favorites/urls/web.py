from django.urls import path
from apps.favorites.controllers.web.favorites import FavoritesListView, FavoriteToggleView

urlpatterns = [
    path('', FavoritesListView.as_view(), name='favorites_list'),
    path('toggle/<int:listing_id>/', FavoriteToggleView.as_view(), name='favorite_toggle'),
]
