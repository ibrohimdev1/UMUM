from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Chat(models.Model):
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='chats',
        verbose_name=_('Tegishli e‘lon')
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buyer_chats',
        verbose_name=_('Xaridor')
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_chats',
        verbose_name=_('Sotuvchi')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chatlar')
        unique_together = ('listing', 'buyer')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat #{self.id}: {self.buyer} <-> {self.seller} ({self.listing.title})"
