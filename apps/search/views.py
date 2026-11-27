from django.views.generic import ListView
from apps.listings.repositories.listing_repository import ListingRepository
from apps.categories.repositories.category_repository import CategoryRepository

class SearchResultsView(ListView):
    template_name = 'listings/list.html'
    context_object_name = 'listings'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        city = self.request.GET.get('city')
        ordering = self.request.GET.get('ordering', '-created_at')

        return ListingRepository.search(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            city=city,
            ordering=ordering
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryRepository.get_all_root()
        context['query'] = self.request.GET.get('q', '')
        return context
