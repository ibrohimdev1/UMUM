from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.favorites.services.favorite_service import FavoriteService

class FavoritesListView(LoginRequiredMixin, View):
    template_name = 'favorites/list.html'

    def get(self, request):
        favorites = FavoriteService.get_favorites(request.user)
        return render(request, self.template_name, {'favorites': favorites})

class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, listing_id):
        res = FavoriteService.toggle(request.user, listing_id)
        messages.info(request, res['message'])
        return redirect(request.META.get('HTTP_REFERER', 'home'))
