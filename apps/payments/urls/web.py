from django.urls import path
from apps.payments.controllers.web.payments import (
    PaymentCheckoutView,
    PaymentSuccessView,
    DemoPaymentProcessView
)

urlpatterns = [
    path('checkout/<int:listing_id>/', PaymentCheckoutView.as_view(), name='payment_checkout'),
    path('demo-pay/<int:order_id>/', DemoPaymentProcessView.as_view(), name='demo_payment_process'),
    path('success/<int:order_id>/', PaymentSuccessView.as_view(), name='payment_success'),
]
