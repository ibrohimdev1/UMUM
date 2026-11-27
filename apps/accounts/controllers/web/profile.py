from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.accounts.forms.auth_forms import UserProfileForm, SellerProfileForm
from apps.accounts.services.user_service import UserProfileService, SellerProfileService

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi.')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

class SellerProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/seller_profile.html'

    def get(self, request):
        initial = {
            'full_name': request.user.full_name,
            'city': request.user.city
        }
        form = SellerProfileForm(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SellerProfileForm(request.POST)
        if form.is_valid():
            SellerProfileService.complete_seller_profile(
                request.user,
                full_name=form.cleaned_data['full_name'],
                city=form.cleaned_data['city']
            )
            messages.success(request, 'Sotuvchi profili to‘ldirildi! Endi bemalol e‘lon berishingiz mumkin.')
            next_url = request.GET.get('next', 'listing_create')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})
