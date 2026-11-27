from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.categories.models import Category
from apps.listings.models import Listing, ListingImage

class Command(BaseCommand):
    help = 'Seeds initial categories and demo data for UMUM platform'

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # 1. Admin Superuser
        admin_user, created = User.objects.get_or_create(
            phone='+998901234567',
            defaults={
                'full_name': 'Bosh Administrator',
                'is_staff': True,
                'is_superuser': True,
                'role': User.Role.ADMIN,
                'status': User.Status.ACTIVE,
                'seller_profile_completed': True,
                'city': 'Toshkent'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created: phone=+998901234567, pass=admin123"))

        # 2. Demo Seller User
        seller, _ = User.objects.get_or_create(
            phone='+998939876543',
            defaults={
                'full_name': 'Ibrohim Hasanov',
                'role': User.Role.USER,
                'status': User.Status.ACTIVE,
                'seller_profile_completed': True,
                'city': 'Samarqand'
            }
        )

        # 3. Categories
        categories_data = [
            {'name': 'Avtomobillar', 'icon': 'fas fa-car', 'order': 1},
            {'name': 'Ko‘chmas mulk', 'icon': 'fas fa-home', 'order': 2},
            {'name': 'Elektronika', 'icon': 'fas fa-laptop', 'order': 3},
            {'name': 'Xizmatlar', 'icon': 'fas fa-tools', 'order': 4},
            {'name': 'Ish o‘rinlari', 'icon': 'fas fa-briefcase', 'order': 5},
            {'name': 'Moda va Kiyimlar', 'icon': 'fas fa-tshirt', 'order': 6},
        ]

        cats = {}
        for c_data in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=c_data['name'],
                defaults={'icon': c_data['icon'], 'order': c_data['order']}
            )
            cats[c_data['name']] = cat

        # 4. Sample Active Listings
        sample_listings = [
            {
                'title': 'Chevrolet Cobalt 4-pozitsiya avtomat',
                'category': cats['Avtomobillar'],
                'price': 138000000,
                'city': 'Toshkent',
                'address': 'Chilonzor tumani, Bunyodkor ko‘chasi',
                'lat': 41.2825,
                'lng': 69.2150,
                'description': '2023-yil, probeg 15000 km. Holati ideal, kraskasi toza. Gaz o‘rnatilmagan, faqat benzinda yurgan.',
            },
            {
                'title': 'iPhone 15 Pro Max 256GB Natural Titanium',
                'category': cats['Elektronika'],
                'price': 13500000,
                'city': 'Tashkent',
                'address': 'Malika bozor, A-blok',
                'lat': 41.3400,
                'lng': 69.2600,
                'description': 'Yangi, karobka-dokument ochilmagan. Batareya 100%, original zaryad kabeli bor.',
            },
            {
                'title': '3 xonali shinam kvartira Yunusobod 14',
                'category': cats['Ko‘chmas mulk'],
                'price': 850000000,
                'city': 'Toshkent',
                'address': 'Yunusobod 14-mavze',
                'lat': 41.3650,
                'lng': 69.2890,
                'description': 'Evro remont, mebellari bilan birga sotiladi. Maktab, bog‘cha, metro yaqinida.',
            },
            {
                'title': 'Professional veb-sayt va bot yaratish',
                'category': cats['Xizmatlar'],
                'price': 2500000,
                'city': 'Samarqand',
                'address': 'Registon yaqinida',
                'lat': 39.6542,
                'lng': 66.9597,
                'description': 'Har qanday murakkablikdagi Python, Django va Telegram bot xizmatlari. Kafolat beriladi.',
            }
        ]

        for s in sample_listings:
            l, created = Listing.objects.get_or_create(
                title=s['title'],
                defaults={
                    'user': seller,
                    'category': s['category'],
                    'price': s['price'],
                    'city': s['city'],
                    'address': s['address'],
                    'lat': s['lat'],
                    'lng': s['lng'],
                    'description': s['description'],
                    'status': Listing.Status.ACTIVE
                }
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))
