from django.urls import path
from apps.orders.controllers.api.orders import OrderCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path('', OrderCreateAPIView.as_view(), name='api_orders_create'),
    path('<int:pk>', OrderDetailAPIView.as_view(), name='api_orders_detail'),
]
