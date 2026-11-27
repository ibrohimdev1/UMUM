from django.core.exceptions import ValidationError
from apps.orders.repositories.order_repository import OrderRepository
from apps.listings.repositories.listing_repository import ListingRepository

class OrderService:
    @classmethod
    def create_order(cls, user, listing_id):
        listing = ListingRepository.get_by_id(listing_id, only_active=True)
        if not listing:
            raise ValidationError('Faol e‘lon topilmadi.')

        if listing.user_id == user.id:
            raise ValidationError('O‘z e‘loningizni sotib ola olmaysiz.')

        order = OrderRepository.create_order(
            listing=listing,
            buyer=user,
            amount=listing.price
        )
        return order

    @classmethod
    def get_order_details(cls, user, order_id):
        order = OrderRepository.get_by_id(order_id)
        if not order:
            raise ValidationError('Buyurtma topilmadi.')
        if order.buyer_id != user.id and order.listing.user_id != user.id and not user.is_staff:
            raise ValidationError('Ruxsat etilmagan buyurtma.')
        return order
