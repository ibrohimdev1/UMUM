from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.accounts.forms.auth_forms import OTPVerifyForm
from apps.accounts.services.auth_service import AuthService
from apps.accounts.services.google_auth import GoogleAuthService

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

        # One-click Social Logins with specific account data
        social = request.GET.get('social')
        if social in ['google', 'facebook', 'apple']:
            social_name = social.capitalize()
            email = request.GET.get('email', '').strip().lower() or f"{social}.user@umum.uz"
            name = request.GET.get('name', '').strip() or f"{social_name} Foydalanuvchisi"

            # Check if an account already exists with this email
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                # 1. AUTO-REGISTER new user via Social/Google
                dummy_phone = f"+99899{abs(hash(email)) % 9000000 + 1000000}"
                while User.objects.filter(phone=dummy_phone).exists():
                    dummy_phone = f"+99899{abs(hash(dummy_phone + 'g')) % 9000000 + 1000000}"
                user = User.objects.create_user(
                    phone=dummy_phone,
                    email=email,
                    full_name=name,
                    status=User.Status.ACTIVE
                )
                messages.success(request, f"Xush kelibsiz! Siz {social_name} ({email}) orqali muvaffaqiyatli ro‘yxatdan o‘tdingiz.")
            else:
                # 2. LOGIN existing user via Social/Google
                if name and not user.full_name:
                    user.full_name = name
                    user.save(update_fields=['full_name'])
                messages.success(request, f"Xush kelibsiz, {user.full_name or user.email}! {social_name} orqali hisobingizga kirdingiz.")

            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or 'home')

        return render(request, self.template_name, {
            'next': request.GET.get('next', ''),
            'tab': request.GET.get('tab', 'login'),
            'google_configured': GoogleAuthService.is_configured()
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

class GoogleLoginView(View):
    """
    Initiates Google OAuth 2.0 flow if configured in .env,
    otherwise renders the interactive Google account chooser dialog.
    """
    def get(self, request):
        if GoogleAuthService.is_configured():
            auth_url = GoogleAuthService.get_authorization_url(request)
            return redirect(auth_url)
        # If not configured with Google Cloud yet, trigger the account selector
        return redirect('/auth/login/?open_google=1')

class GoogleCallbackView(View):
    """
    Handles redirect callback from Google OAuth 2.0 servers.
    """
    def get(self, request):
        code = request.GET.get('code')
        error = request.GET.get('error')
        if error or not code:
            messages.error(request, "Google orqali kirish bekor qilindi yoki xatolik yuz berdi.")
            return redirect('auth_login')

        try:
            user_info = GoogleAuthService.exchange_code_for_user_info(code, request)
            if not user_info or not user_info.get('email'):
                messages.error(request, "Google profil ma’lumotlarini olishda xatolik yuz berdi.")
                return redirect('auth_login')

            email = user_info['email'].lower()
            name = user_info.get('name', 'Google Foydalanuvchisi')

            # Find or auto-register user
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                dummy_phone = f"+99899{abs(hash(email)) % 9000000 + 1000000}"
                while User.objects.filter(phone=dummy_phone).exists():
                    dummy_phone = f"+99899{abs(hash(dummy_phone + 'g')) % 9000000 + 1000000}"
                user = User.objects.create_user(
                    phone=dummy_phone,
                    email=email,
                    full_name=name,
                    status=User.Status.ACTIVE
                )
                messages.success(request, f"Xush kelibsiz! Google ({email}) orqali ro‘yxatdan o‘tdingiz.")
            else:
                messages.success(request, f"Xush kelibsiz, {user.full_name or user.email}! Google orqali hisobingizga kirdingiz.")

            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Google tizimi bilan aloqada xatolik: {e}")
            return redirect('auth_login')

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
