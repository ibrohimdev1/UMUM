from django.db.models import Sum, Count
from apps.accounts.models import User
from apps.listings.models import Listing
from apps.orders.models import Order
from apps.payments.models import Payment

class AnalyticsService:
    @classmethod
    def get_system_stats(cls):
        return {
            'total_users': User.objects.count(),
            'total_listings': Listing.objects.count(),
            'active_listings': Listing.objects.filter(status=Listing.Status.ACTIVE).count(),
            'pending_moderation': Listing.objects.filter(status=Listing.Status.MODERATION).count(),
            'total_orders': Order.objects.count(),
            'paid_orders': Order.objects.filter(status=Order.Status.PAID).count(),
            'total_revenue': Payment.objects.filter(status=Payment.Status.PERFORMED).aggregate(Sum('amount'))['amount__sum'] or 0,
        }
