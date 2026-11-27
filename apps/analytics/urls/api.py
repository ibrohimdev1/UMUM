from django.urls import path
from apps.analytics.controllers.api.analytics import (
    AdminUsersAPIView,
    AdminUserDetailAPIView,
    AdminStatsAPIView
)

urlpatterns = [
    path('users', AdminUsersAPIView.as_view(), name='api_admin_users'),
    path('users/<int:pk>', AdminUserDetailAPIView.as_view(), name='api_admin_user_detail'),
    path('stats', AdminStatsAPIView.as_view(), name='api_admin_stats'),
]
