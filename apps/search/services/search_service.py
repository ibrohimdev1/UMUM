from apps.listings.repositories.listing_repository import ListingRepository

class SearchService:
    @classmethod
    def search_listings(cls, query=None, category_id=None, min_price=None, max_price=None, city=None, ordering='-created_at'):
        return ListingRepository.search(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            city=city,
            ordering=ordering
        )
