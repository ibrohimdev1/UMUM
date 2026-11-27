from django.contrib import admin
from apps.accounts.models import User, OTPVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', 'role', 'status', 'city', 'seller_profile_completed', 'created_at')
    list_filter = ('role', 'status', 'seller_profile_completed', 'created_at')
    search_fields = ('phone', 'full_name', 'city')
    ordering = ('-created_at',)
    fieldsets = (
        ('Asosiy ma‘lumotlar', {'fields': ('phone', 'full_name', 'email', 'avatar')}),
        ('Rollar va Huquqlar', {'fields': ('role', 'status', 'is_staff', 'is_superuser')}),
        ('Sotuvchi sozlamalari', {'fields': ('city', 'seller_profile_completed')}),
        ('Tizim sanalari', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'is_used', 'attempts', 'expires_at', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone', 'code')
    readonly_fields = ('created_at',)
