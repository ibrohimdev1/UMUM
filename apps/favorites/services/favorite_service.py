from apps.favorites.repositories.favorite_repository import FavoriteRepository
from apps.listings.repositories.listing_repository import ListingRepository
from django.core.exceptions import ValidationError

class FavoriteService:
    @classmethod
    def toggle(cls, user, listing_id):
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValidationError('E‘lon topilmadi.')

        if FavoriteRepository.is_favorited(user, listing_id):
            FavoriteRepository.remove(user, listing_id)
            return {'favorited': False, 'message': 'Sevimlilardan o‘chirildi'}
        else:
            FavoriteRepository.add(user, listing_id)
            return {'favorited': True, 'message': 'Sevimlilarga qo‘shildi'}

    @classmethod
    def get_favorites(cls, user):
        return FavoriteRepository.get_user_favorites(user)
