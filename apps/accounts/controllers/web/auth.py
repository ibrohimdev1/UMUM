from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.accounts.forms.auth_forms import LoginForm, OTPVerifyForm
from apps.accounts.services.auth_service import AuthService

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            try:
                AuthService.request_otp(phone)
                request.session['auth_phone'] = phone
                return redirect('auth_verify')
            except ValidationError as e:
                messages.error(request, str(e.message if hasattr(e, 'message') else e))
        return render(request, self.template_name, {'form': form})

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
                del request.session['auth_phone']
                messages.success(request, f"Xush kelibsiz, {user.full_name or user.phone}!")
                
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            except ValidationError as e:
                messages.error(request, str(e.message if hasattr(e, 'message') else e))
        return render(request, self.template_name, {'form': form, 'phone': phone})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
        return redirect('home')
