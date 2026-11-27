from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Foydalanuvchi')
    )
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=_('E‘lon')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Sevimli e‘lon')
        verbose_name_plural = _('Sevimlilar')
        unique_together = ('user', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.listing.title}"
