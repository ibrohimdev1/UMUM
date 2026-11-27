from apps.listings.models import Listing
from apps.notifications.services.notification_service import NotificationService
from apps.audit.services.audit_service import AuditService

class ModerationService:
    @classmethod
    def get_pending_listings(cls):
        return Listing.objects.filter(status=Listing.Status.MODERATION).select_related('user', 'category').prefetch_related('images').order_by('created_at')

    @classmethod
    def approve(cls, listing_id, admin_user):
        listing = Listing.objects.get(id=listing_id)
        listing.status = Listing.Status.ACTIVE
        listing.reject_reason = None
        listing.save(update_fields=['status', 'reject_reason'])

        AuditService.log_action(action='MODERATION_APPROVE', entity=f'Listing:{listing.id}', actor=admin_user)
        NotificationService.notify_user(listing.user, f"Tabriklaymiz! Sizning '{listing.title}' nomli e‘loningiz tasdiqlandi va faollashtirildi.")
        return listing

    @classmethod
    def reject(cls, listing_id, reason, admin_user):
        listing = Listing.objects.get(id=listing_id)
        listing.status = Listing.Status.REJECTED
        listing.reject_reason = reason
        listing.save(update_fields=['status', 'reject_reason'])

        AuditService.log_action(action='MODERATION_REJECT', entity=f'Listing:{listing.id}', actor=admin_user, extra_data={'reason': reason})
        NotificationService.notify_user(listing.user, f"E‘loningiz rad etildi: '{listing.title}'. Sababi: {reason}")
        return listing
