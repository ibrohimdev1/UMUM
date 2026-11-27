from django.urls import path
from apps.accounts.controllers.api.auth import RequestCodeAPIView, VerifyCodeAPIView

urlpatterns = [
    path('request-code', RequestCodeAPIView.as_view(), name='api_auth_request_code'),
    path('verify', VerifyCodeAPIView.as_view(), name='api_auth_verify'),
]
