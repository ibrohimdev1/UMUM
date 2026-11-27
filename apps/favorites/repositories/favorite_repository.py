from apps.favorites.models import Favorite

class FavoriteRepository:
    @staticmethod
    def get_user_favorites(user):
        return Favorite.objects.filter(user=user).select_related('listing', 'listing__user', 'listing__category').prefetch_related('listing__images')

    @staticmethod
    def is_favorited(user, listing_id):
        if not user or not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, listing_id=listing_id).exists()

    @staticmethod
    def add(user, listing_id):
        fav, _ = Favorite.objects.get_or_create(user=user, listing_id=listing_id)
        return fav

    @staticmethod
    def remove(user, listing_id):
        Favorite.objects.filter(user=user, listing_id=listing_id).delete()
