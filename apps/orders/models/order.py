from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Kutilmoqda')
        PAID = 'PAID', _('To‘langan')
        FAILED = 'FAILED', _('Muvaffaqiyatsiz')
        CANCELLED = 'CANCELLED', _('Bekor qilingan')
        REFUNDED = 'REFUNDED', _('Qaytarilgan')

    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('E‘lon')
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Xaridor')
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_('Summa (UZS)'))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name=_('Holat')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Buyurtma')
        verbose_name_plural = _('Buyurtmalar')
        ordering = ['-created_at']

    @property
    def formatted_amount(self):
        try:
            val = int(round(float(self.amount)))
            return f"{val:,}".replace(",", " ")
        except (ValueError, TypeError):
            return f"{self.amount}"

    def __str__(self):
        return f"Order #{self.id}: {self.listing.title} - {self.amount} UZS ({self.get_status_display()})"
