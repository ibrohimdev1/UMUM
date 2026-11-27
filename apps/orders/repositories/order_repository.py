from apps.orders.models import Order

class OrderRepository:
    @staticmethod
    def create_order(listing, buyer, amount):
        return Order.objects.create(
            listing=listing,
            buyer=buyer,
            amount=amount,
            status=Order.Status.PENDING
        )

    @staticmethod
    def get_by_id(order_id):
        return Order.objects.select_related('listing', 'buyer', 'listing__user').filter(id=order_id).first()

    @staticmethod
    def update_status(order, status):
        order.status = status
        order.save(update_fields=['status', 'updated_at'])
        return order
