from django.contrib import admin
from apps.orders.models import Order
from apps.payments.models import Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'buyer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'buyer__phone', 'listing__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payme_ref', 'amount', 'status', 'created_at', 'performed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payme_ref', 'order__id')
    readonly_fields = ('created_at', 'performed_at')
