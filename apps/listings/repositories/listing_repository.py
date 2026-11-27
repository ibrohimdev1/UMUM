from django.db.models import Q
from apps.listings.models import Listing, ListingImage

class ListingRepository:
    @staticmethod
    def get_active_listings():
        return Listing.objects.filter(status=Listing.Status.ACTIVE).select_related('user', 'category').prefetch_related('images').order_by('-created_at')

    @staticmethod
    def get_by_id(listing_id, only_active=False):
        qs = Listing.objects.select_related('user', 'category').prefetch_related('images')
        if only_active:
            qs = qs.filter(status=Listing.Status.ACTIVE)
        return qs.filter(id=listing_id).first()

    @staticmethod
    def get_user_listings(user):
        return Listing.objects.filter(user=user).select_related('category').prefetch_related('images').order_by('-created_at')

    @staticmethod
    def get_map_listings():
        return Listing.objects.filter(
            status=Listing.Status.ACTIVE,
            lat__isnull=False,
            lng__isnull=False
        ).select_related('category').prefetch_related('images')

    @staticmethod
    def create_listing(user, category, title, description, price, lat=None, lng=None, city='', address='', status=Listing.Status.MODERATION):
        return Listing.objects.create(
            user=user,
            category=category,
            title=title,
            description=description,
            price=price,
            lat=lat,
            lng=lng,
            city=city,
            address=address,
            status=status
        )

    @staticmethod
    def add_image(listing, image_file=None, url='', position=0):
        return ListingImage.objects.create(
            listing=listing,
            image=image_file,
            url=url,
            position=position
        )

    @staticmethod
    def search(query=None, category_id=None, min_price=None, max_price=None, city=None, ordering='-created_at'):
        qs = Listing.objects.filter(status=Listing.Status.ACTIVE).select_related('user', 'category').prefetch_related('images')

        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if category_id:
            qs = qs.filter(Q(category_id=category_id) | Q(category__parent_id=category_id))

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        if city:
            qs = qs.filter(city__icontains=city)

        valid_orderings = {
            'newest': '-created_at',
            'oldest': 'created_at',
            'price_asc': 'price',
            'price_desc': '-price',
        }
        order_field = valid_orderings.get(ordering, '-created_at')
        return qs.order_by(order_field)
