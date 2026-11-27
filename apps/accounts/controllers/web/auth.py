from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.accounts.forms.auth_forms import OTPVerifyForm
from apps.accounts.services.auth_service import AuthService

User = get_user_model()

def normalize_identifier(identifier: str):
    """
    Normalizes phone numbers and emails.
    Supports +998901234567, 901234567, 998901234567, or user@example.com
    """
    raw = identifier.strip()
    if '@' in raw:
        return 'email', raw.lower()
    digits = ''.join(c for c in raw if c.isdigit())
    if len(digits) == 9:
        return 'phone', f"+998{digits}"
    elif len(digits) == 12 and digits.startswith('998'):
        return 'phone', f"+{digits}"
    elif raw.startswith('+'):
        return 'phone', f"+{digits}"
    return 'phone', raw

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        # One-click Social Demo Logins
        social = request.GET.get('social')
        if social in ['google', 'facebook', 'apple']:
            social_name = social.capitalize()
            dummy_phone = f"+99899{abs(hash(social)) % 9000000 + 1000000}"
            user, _ = User.objects.get_or_create(
                phone=dummy_phone,
                defaults={
                    'full_name': f"{social_name} Foydalanuvchisi",
                    'email': f"{social}.user@umum.uz",
                    'status': User.Status.ACTIVE
                }
            )
            login(request, user)
            messages.success(request, f"{social_name} orqali tizimga kirdingiz!")
            next_url = request.GET.get('next')
            return redirect(next_url or 'home')

        return render(request, self.template_name, {
            'next': request.GET.get('next', ''),
            'tab': request.GET.get('tab', 'login')
        })

    def post(self, request):
        action = request.POST.get('action', 'login')
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()
        next_url = request.POST.get('next') or request.GET.get('next') or 'home'

        if not identifier:
            messages.error(request, "Iltimos, elektron pochta yoki telefon raqamingizni kiriting.")
            return render(request, self.template_name, {'identifier': identifier, 'tab': action})

        id_type, clean_id = normalize_identifier(identifier)

        # ----------------------------------------------------------------------
        # 1. REGISTRATION TAB
        # ----------------------------------------------------------------------
        if action == 'register':
            if not password or len(password) < 6:
                messages.error(request, "Parol kamida 6 ta belgidan iborat bo‘lishi kerak.")
                return render(request, self.template_name, {'identifier': identifier, 'tab': 'register'})

            # Check if user already exists
            user = None
            if id_type == 'email':
                user = User.objects.filter(email__iexact=clean_id).first()
            else:
                user = User.objects.filter(phone=clean_id).first()

            if user:
                messages.warning(request, "Ushbu telefon yoki email bilan allaqachon ro‘yxatdan o‘tilgan. Tizimga kiring.")
                return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})

            # Create new user
            if id_type == 'phone':
                new_user = User.objects.create_user(phone=clean_id, password=password)
            else:
                dummy_phone = f"+998{abs(hash(clean_id)) % 900000000 + 100000000}"
                new_user = User.objects.create_user(phone=dummy_phone, email=clean_id, password=password)

            login(request, new_user)
            messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi! Xush kelibsiz.")
            return redirect(next_url)

        # ----------------------------------------------------------------------
        # 2. LOGIN TAB (Password or SMS)
        # ----------------------------------------------------------------------
        if action == 'sms_request':
            if id_type != 'phone':
                messages.error(request, "SMS tasdiqlash kodi faqat telefon raqamiga yuboriladi.")
                return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})
            try:
                AuthService.request_otp(clean_id)
                request.session['auth_phone'] = clean_id
                return redirect('auth_verify')
            except ValidationError as e:
                messages.error(request, str(e.message if hasattr(e, 'message') else e))
                return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})

        # Standard Password Login
        if not password:
            messages.error(request, "Iltimos, parolingizni kiriting.")
            return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})

        user = None
        if id_type == 'email':
            user = User.objects.filter(email__iexact=clean_id).first()
        else:
            user = User.objects.filter(phone=clean_id).first()

        if user and user.check_password(password):
            if user.status == User.Status.BLOCKED:
                messages.error(request, "Ushbu hisob bloklangan. Administrator bilan bog‘laning.")
                return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.full_name or user.phone}!")
            return redirect(next_url)
        else:
            messages.error(request, "Elektron pochta/telefon yoki parol noto‘g‘ri kiritildi.")
            return render(request, self.template_name, {'identifier': identifier, 'tab': 'login'})

class VerifyOTPView(View):
    template_name = 'accounts/verify.html'

    def get(self, request):
        phone = request.session.get('auth_phone')
        if not phone:
            return redirect('auth_login')
        form = OTPVerifyForm(initial={'phone': phone})
        return render(request, self.template_name, {'form': form, 'phone': phone})

    def post(self, request):
        phone = request.session.get('auth_phone')
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                result = AuthService.verify_otp(phone, code)
                user = result['user']
                login(request, user)
                if 'auth_phone' in request.session:
                    del request.session['auth_phone']
                messages.success(request, f"Xush kelibsiz, {user.full_name or user.phone}!")
                next_url = request.GET.get('next')
                return redirect(next_url or 'home')
            except ValidationError as e:
                messages.error(request, str(e.message if hasattr(e, 'message') else e))
        return render(request, self.template_name, {'form': form, 'phone': phone})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
        return redirect('home')
