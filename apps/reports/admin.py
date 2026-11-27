from django.contrib import admin
from apps.reports.models import Report
from apps.audit.models import AuditLog
from apps.notifications.models import Notification

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'reported_user', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reason', 'description', 'user__phone')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'actor', 'action', 'entity', 'ip_address')
    list_filter = ('action', 'created_at')
    search_fields = ('action', 'entity', 'actor__phone')
    readonly_fields = ('created_at', 'actor', 'action', 'entity', 'ip_address', 'extra_data')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'channel', 'body', 'is_read', 'sent_at')
    list_filter = ('channel', 'is_read', 'sent_at')
    search_fields = ('user__phone', 'body')
