from apps.categories.models import Category

class CategoryRepository:
    @staticmethod
    def get_all_root():
        return Category.objects.filter(parent__isnull=True).prefetch_related('children').order_by('order', 'name')

    @staticmethod
    def get_all():
        return Category.objects.all().order_by('order', 'name')

    @staticmethod
    def get_by_id(category_id):
        return Category.objects.filter(id=category_id).first()
