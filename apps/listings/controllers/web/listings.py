from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.listings.forms.listing_forms import ListingForm
from apps.listings.repositories.listing_repository import ListingRepository
from apps.listings.services.listing_service import ListingService
from apps.categories.repositories.category_repository import CategoryRepository

class ListingListView(View):
    template_name = 'listings/list.html'

    def get(self, request):
        query = request.GET.get('q')
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        city = request.GET.get('city')
        ordering = request.GET.get('ordering', '-created_at')

        listings = ListingRepository.search(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            city=city,
            ordering=ordering
        )
        return render(request, self.template_name, {
            'listings': listings,
            'categories': CategoryRepository.get_all_root(),
            'query': query,
            'selected_category': category_id,
        })

class ListingDetailView(View):
    template_name = 'listings/detail.html'

    def get(self, request, pk):
        listing = get_object_or_404(ListingRepository.get_active_listings(), id=pk)
        ListingService.increment_view(listing.id)
        return render(request, self.template_name, {'listing': listing})

class ListingCreateView(LoginRequiredMixin, View):
    template_name = 'listings/create.html'

    def get(self, request):
        # FR-22 check: if seller profile not completed, redirect to seller profile setup
        if not request.user.seller_profile_completed:
            messages.info(request, "E‘lon joylashdan oldin sotuvchi profilingizni to‘ldiring (FR-22).")
            return redirect('seller_profile')

        form = ListingForm(initial={'city': request.user.city})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.seller_profile_completed:
            return redirect('seller_profile')

        form = ListingForm(request.POST)
        files = request.FILES.getlist('images')

        if form.is_valid():
            try:
                listing = ListingService.create_listing(
                    user=request.user,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    price=form.cleaned_data['price'],
                    category_id=form.cleaned_data['category'].id,
                    lat=form.cleaned_data.get('lat'),
                    lng=form.cleaned_data.get('lng'),
                    city=form.cleaned_data.get('city'),
                    address=form.cleaned_data.get('address'),
                    images=files
                )
                messages.success(request, "E‘loningiz qabul qilindi va moderatsiyaga yuborildi!")
                return redirect('my_listings')
            except ValidationError as e:
                messages.error(request, str(e.message if hasattr(e, 'message') else e))
        return render(request, self.template_name, {'form': form})

class MyListingsView(LoginRequiredMixin, View):
    template_name = 'listings/my_listings.html'

    def get(self, request):
        listings = ListingRepository.get_user_listings(request.user)
        return render(request, self.template_name, {'listings': listings})

class MapView(View):
    template_name = 'map/map.html'

    def get(self, request):
        return render(request, self.template_name)
