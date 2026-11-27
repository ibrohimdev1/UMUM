from apps.reports.models import Report
from django.core.exceptions import ValidationError

class ReportRepository:
    @staticmethod
    def create(user, reason, description='', listing=None, reported_user=None):
        return Report.objects.create(
            user=user,
            listing=listing,
            reported_user=reported_user,
            reason=reason,
            description=description,
            status=Report.Status.OPEN
        )

    @staticmethod
    def get_open_reports():
        return Report.objects.filter(status=Report.Status.OPEN).select_related('user', 'listing', 'reported_user').order_by('-created_at')

class ReportService:
    @classmethod
    def submit_report(cls, user, reason, description='', listing_id=None, reported_user_id=None):
        from apps.listings.repositories.listing_repository import ListingRepository
        from apps.accounts.repositories.user_repository import UserRepository

        listing = ListingRepository.get_by_id(listing_id) if listing_id else None
        reported_user = UserRepository.get_by_id(reported_user_id) if reported_user_id else None

        if not listing and not reported_user:
            raise ValidationError('E‘lon yoki foydalanuvchi ko‘rsatilishi shart.')

        if listing and Report.objects.filter(user=user, listing=listing, status=Report.Status.OPEN).exists():
            raise ValidationError('Siz ushbu e‘lon bo‘yicha allaqachon shikoyat yuborgansiz.')

        return ReportRepository.create(
            user=user,
            listing=listing,
            reported_user=reported_user,
            reason=reason,
            description=description
        )
