from django.db import models
from django.utils.translation import gettext_lazy as _

class Payment(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', _('Yaratilgan')
        PERFORMED = 'PERFORMED', _('Bajarilgan')
        CANCELLED = 'CANCELLED', _('Bekor qilingan')
        FAILED = 'FAILED', _('Xato')

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Buyurtma')
    )
    payme_ref = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_('Payme Tranzaksiya ID')
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_('Summa'))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
        db_index=True,
        verbose_name=_('Holat')
    )
    cancel_reason = models.IntegerField(null=True, blank=True, verbose_name=_('Bekor qilish sababi kodi'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    performed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Amalga oshirilgan vaqti'))

    class Meta:
        verbose_name = _('To‘lov')
        verbose_name_plural = _('To‘lovlar')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order_id}: {self.amount} UZS ({self.status})"
