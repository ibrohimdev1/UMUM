from django.contrib import admin
from django.utils.html import format_html
from apps.listings.models import Listing, ListingImage
from apps.moderation.services.moderation_service import ModerationService

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ('image', 'position')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'price_display', 'is_promotion', 'promotion_text',
        'user', 'category', 'status_badge', 'city', 'views_count', 'created_at'
    )
    list_editable = ('is_promotion',)
    list_filter = ('is_promotion', 'status', 'category', 'city', 'created_at')
    search_fields = ('title', 'description', 'user__phone', 'user__full_name')
    inlines = [ListingImageInline]
    actions = ['approve_listings', 'reject_listings', 'enable_promotion', 'disable_promotion']
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    def price_display(self, obj):
        if obj.old_price:
            return format_html(
                f'<span style="text-decoration: line-through; color: #888; font-size: 0.85em;">{obj.old_price:,.0f} UZS</span><br>'
                f'<strong style="color: #0d6efd;">{obj.price:,.0f} UZS</strong>'
            )
        return format_html(f'<strong>{obj.price:,.0f} UZS</strong>')
    price_display.short_description = "Narx"

    def status_badge(self, obj):
        colors = {
            'ACTIVE': 'green',
            'MODERATION': 'orange',
            'REJECTED': 'red',
            'DRAFT': 'gray',
            'ARCHIVED': 'black',
            'SOLD': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(f'<span style="color: white; background-color: {color}; padding: 3px 8px; border-radius: 10px; font-weight: bold;">{obj.status}</span>')
    status_badge.short_description = "Holat"

    @admin.action(description="Tanlangan e‘lonlarni TASDIQLASH (ACTIVE qilish)")
    def approve_listings(self, request, queryset):
        for listing in queryset:
            ModerationService.approve(listing.id, request.user)
        self.message_user(request, f"{queryset.count()} ta e‘lon muvaffaqiyatli tasdiqlandi.")

    @admin.action(description="Tanlangan e‘lonlarni RAD ETISH")
    def reject_listings(self, request, queryset):
        for listing in queryset:
            ModerationService.reject(listing.id, "Platforma qoidalariga mos kelmadi.", request.user)
        self.message_user(request, f"{queryset.count()} ta e‘lon rad etildi.")

    @admin.action(description="Tanlangan e‘lonlarga AKSIYA belgisini yoqish")
    def enable_promotion(self, request, queryset):
        count = queryset.update(is_promotion=True)
        self.message_user(request, f"{count} ta e‘londa AKSIYA belgisi yoqildi.")

    @admin.action(description="Tanlangan e‘lonlardan AKSIYA belgisini o‘chirish")
    def disable_promotion(self, request, queryset):
        count = queryset.update(is_promotion=False)
        self.message_user(request, f"{count} ta e‘londan AKSIYA belgisi o‘chirildi.")
