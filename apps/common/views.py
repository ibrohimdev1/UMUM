from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from django.utils import translation
from apps.listings.repositories.listing_repository import ListingRepository
from apps.categories.repositories.category_repository import CategoryRepository

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_listings'] = ListingRepository.get_active_listings()[:12]
        context['categories'] = CategoryRepository.get_all_root()
        return context

def set_language_view(request, lang_code):
    """
    Switches language (uz, ru, en) and stores choice in session & cookie with path='/' (FR-19).
    """
    if lang_code in ['uz', 'ru', 'en']:
        request.session['django_language'] = lang_code
        request.session.modified = True
        translation.activate(lang_code)
        cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
        referrer = request.META.get('HTTP_REFERER') or '/'
        response = redirect(referrer)
        response.set_cookie(cookie_name, lang_code, max_age=365 * 24 * 60 * 60, path='/')
        return response
    return redirect('/')
