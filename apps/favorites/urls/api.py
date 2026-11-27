from django.urls import path
from apps.favorites.controllers.api.favorites import FavoriteAPIView

urlpatterns = [
    path('<int:listing_id>', FavoriteAPIView.as_view(), name='api_favorite_action'),
]
