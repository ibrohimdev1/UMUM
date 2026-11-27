import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.orders.models import Order
from apps.orders.services.order_service import OrderService
from apps.payments.models import Payment
from apps.notifications.services.notification_service import NotificationService

class PaymentCheckoutView(LoginRequiredMixin, View):
    template_name = 'payments/checkout.html'

    def get(self, request, listing_id):
        order = OrderService.create_order(request.user, listing_id)
        return render(request, self.template_name, {
            'order': order,
            'listing': order.listing,
        })

class DemoPaymentProcessView(LoginRequiredMixin, View):
    """
    Demo Payment processor for sandbox/testing without real banking API (FR-13 Demo).
    """
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
        payment_method = request.POST.get('payment_method', 'Payme Demo')
        
        # 1. Update Order status to PAID
        order.status = Order.Status.PAID
        order.save(update_fields=['status', 'updated_at'])

        # 2. Create or update Payment record
        ref = f"DEMO-{uuid.uuid4().hex[:10].upper()}"
        payment = Payment.objects.create(
            order=order,
            payme_ref=ref,
            amount=order.amount,
            status=Payment.Status.PERFORMED,
            performed_at=timezone.now()
        )

        # 3. Send Notification to Buyer and Seller
        NotificationService.notify_user(
            user=order.buyer,
            message=f"To‘lov qabul qilindi! Buyurtma #{order.id} muvaffaqiyatli to‘landi ({payment_method}). Summa: {order.amount:,.0f} UZS.",
            channel='PAYME'
        )

        if order.listing.user != order.buyer:
            NotificationService.notify_user(
                user=order.listing.user,
                message=f"Sizning '{order.listing.title}' e‘loningizga yangi to‘lov qabul qilindi! Buyurtma #{order.id}. Summa: {order.amount:,.0f} UZS.",
                channel='PAYME'
            )

        return redirect('payment_success', order_id=order.id)

class PaymentSuccessView(LoginRequiredMixin, View):
    template_name = 'payments/success.html'

    def get(self, request, order_id):
        order = OrderService.get_order_details(request.user, order_id)
        payment = order.payments.order_by('-created_at').first()
        return render(request, self.template_name, {
            'order': order,
            'payment': payment
        })
