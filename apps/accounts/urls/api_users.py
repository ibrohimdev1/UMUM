from django.urls import path
from apps.accounts.controllers.api.users import UserProfileAPIView

urlpatterns = [
    path('me', UserProfileAPIView.as_view(), name='api_users_me'),
]
