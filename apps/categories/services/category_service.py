from apps.categories.repositories.category_repository import CategoryRepository

class CategoryService:
    @classmethod
    def get_category_tree(cls):
        return CategoryRepository.get_all_root()

    @classmethod
    def get_by_id(cls, category_id):
        return CategoryRepository.get_by_id(category_id)
