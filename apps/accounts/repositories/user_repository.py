from apps.accounts.models import User, OTPVerification

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_phone(phone):
        clean_phone = phone.strip().replace(' ', '')
        return User.objects.filter(phone=clean_phone).first()

    @staticmethod
    def create_user(phone, full_name='', **kwargs):
        clean_phone = phone.strip().replace(' ', '')
        return User.objects.create_user(phone=clean_phone, full_name=full_name, **kwargs)

    @staticmethod
    def update_profile(user, **kwargs):
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def create_otp(phone, code, validity_minutes=2):
        return OTPVerification.generate_otp(phone=phone, code=code, validity_minutes=validity_minutes)

    @staticmethod
    def get_latest_otp(phone):
        clean_phone = phone.strip().replace(' ', '')
        return OTPVerification.objects.filter(phone=clean_phone, is_used=False).order_by('-created_at').first()

    @staticmethod
    def get_all_users():
        return User.objects.all().order_by('-created_at')
