from django.urls import path
from apps.accounts.controllers.web.auth import LoginView, VerifyOTPView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('verify/', VerifyOTPView.as_view(), name='auth_verify'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
