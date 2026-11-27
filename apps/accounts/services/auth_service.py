from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.repositories.user_repository import UserRepository
from integrations.sms.provider import SMSProvider

class AuthService:
    @classmethod
    def request_otp(cls, phone: str) -> dict:
        clean_phone = phone.strip().replace(' ', '')
        if not clean_phone or len(clean_phone) < 9:
            raise ValidationError(_('Yaroqsiz telefon raqami kiritildi.'))

        code = SMSProvider.generate_otp_code()
        UserRepository.create_otp(clean_phone, code)
        SMSProvider.send_sms(clean_phone, f"UMUM platformasiga kirish kodi: {code}")

        return {
            'phone': clean_phone,
            'message': _('SMS tasdiqlash kodi yuborildi.'),
            'debug_code': code  # For quick sandbox testing
        }

    @classmethod
    def verify_otp(cls, phone: str, code: str) -> dict:
        clean_phone = phone.strip().replace(' ', '')
        otp = UserRepository.get_latest_otp(clean_phone)

        if not otp:
            raise ValidationError(_('Tasdiqlash kodi topilmadi yoki eskirgan. Qayta so‘rov yuboring.'))

        if not otp.is_valid():
            raise ValidationError(_('Kodni kiritish muddati o‘tgan yoki urinishlar soni tugagan.'))

        if otp.code != code.strip():
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            raise ValidationError(_('Noto‘g‘ri kod kiritildi.'))

        otp.is_used = True
        otp.save(update_fields=['is_used'])

        user = UserRepository.get_by_phone(clean_phone)
        is_new_user = False
        if not user:
            user = UserRepository.create_user(phone=clean_phone, full_name='')
            is_new_user = True

        # Generate JWT tokens for API / mobile clients
        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'is_new_user': is_new_user,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
