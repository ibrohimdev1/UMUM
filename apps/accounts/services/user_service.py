from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.accounts.repositories.user_repository import UserRepository

class UserProfileService:
    @classmethod
    def update_profile(cls, user, full_name=None, email=None, city=None, avatar=None):
        return UserRepository.update_profile(
            user,
            full_name=full_name,
            email=email,
            city=city,
            avatar=avatar
        )

class SellerProfileService:
    @classmethod
    def complete_seller_profile(cls, user, full_name, city, phone=None):
        if not full_name or not city:
            raise ValidationError(_('To‘liq ism va shahar maydonlari majburiy.'))

        user.full_name = full_name.strip()
        user.city = city.strip()
        user.seller_profile_completed = True
        user.save()
        return user
