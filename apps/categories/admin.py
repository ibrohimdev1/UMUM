from django.contrib import admin
from apps.categories.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'order', 'icon')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('order', 'name')
