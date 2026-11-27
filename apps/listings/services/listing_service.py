from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from apps.listings.models import Listing
from apps.listings.repositories.listing_repository import ListingRepository
from apps.categories.repositories.category_repository import CategoryRepository

class ListingService:
    @classmethod
    def create_listing(cls, user, title, description, price, category_id, lat=None, lng=None, city='', address='', images=None):
        # FR-22: Check seller profile completed
        if not user.seller_profile_completed:
            raise ValidationError(_('E‘lon berishdan avval sotuvchi profilini to‘ldirishingiz lozim (FR-22).'))

        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise ValidationError(_('Tanlangan kategoriya mavjud emas.'))

        with transaction.atomic():
            listing = ListingRepository.create_listing(
                user=user,
                category=category,
                title=title,
                description=description,
                price=price,
                lat=lat,
                lng=lng,
                city=city or user.city,
                address=address,
                status=Listing.Status.MODERATION  # New listings go to MODERATION (FR-15)
            )

            if images:
                for idx, img in enumerate(images):
                    ListingRepository.add_image(listing, image_file=img, position=idx)

        return listing

    @classmethod
    def update_listing(cls, user, listing_id, **kwargs):
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValidationError(_('E‘lon topilmadi.'))

        if listing.user_id != user.id and not user.is_staff:
            raise PermissionDenied(_('Siz boshqa foydalanuvchining e‘lonini tahrirlay olmaysiz.'))

        for key, val in kwargs.items():
            if hasattr(listing, key) and val is not None:
                setattr(listing, key, val)

        # Edited listing goes back to MODERATION
        listing.status = Listing.Status.MODERATION
        listing.save()
        return listing

    @classmethod
    def archive_listing(cls, user, listing_id):
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValidationError(_('E‘lon topilmadi.'))
        if listing.user_id != user.id and not user.is_staff:
            raise PermissionDenied(_('Ruxsat berilmagan.'))

        listing.status = Listing.Status.ARCHIVED
        listing.save(update_fields=['status'])
        return listing

    @classmethod
    def increment_view(cls, listing_id):
        Listing.objects.filter(id=listing_id).update(views_count=models.F('views_count') + 1)
