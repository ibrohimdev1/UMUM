from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Report(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Yangi ochiq')
        REVIEWED = 'REVIEWED', _('Ko‘rib chiqildi')
        CLOSED = 'CLOSED', _('Yopildi')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_submitted',
        verbose_name=_('Shikoyat qiluvchi')
    )
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name=_('Shikoyat qilingan e‘lon')
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports_received',
        verbose_name=_('Shikoyat qilingan shaxs')
    )
    reason = models.CharField(max_length=255, verbose_name=_('Shikoyat sababi'))
    description = models.TextField(blank=True, verbose_name=_('Batafsil izoh'))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
        verbose_name=_('Holat')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))

    class Meta:
        verbose_name = _('Shikoyat')
        verbose_name_plural = _('Shikoyatlar')
        ordering = ['-created_at']

    def __str__(self):
        target = self.listing.title if self.listing else f"User {self.reported_user}"
        return f"Report #{self.id} on {target} ({self.get_status_display()})"
