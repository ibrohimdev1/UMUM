from django.urls import path
from apps.payments.controllers.api.payme import PaymeWebhookAPIView

urlpatterns = [
    path('payme', PaymeWebhookAPIView.as_view(), name='api_payme_webhook'),
]
