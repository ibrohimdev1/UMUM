from django.urls import path
from apps.accounts.controllers.web.auth import (
    LoginView,
    VerifyOTPView,
    LogoutView,
    GoogleLoginView,
    GoogleCallbackView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('verify/', VerifyOTPView.as_view(), name='auth_verify'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('google/login/', GoogleLoginView.as_view(), name='auth_google_login'),
    path('google/callback/', GoogleCallbackView.as_view(), name='auth_google_callback'),
]
