from django.urls import path
from apps.moderation.controllers.api.moderation import (
    ModerationListingListAPIView,
    ModerationListingActionAPIView
)

urlpatterns = [
    path('listings', ModerationListingListAPIView.as_view(), name='api_moderation_listings'),
    path('listings/<int:pk>', ModerationListingActionAPIView.as_view(), name='api_moderation_action'),
]
