from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Qabul qiluvchi')
    )
    channel = models.CharField(max_length=50, default='SMS', verbose_name=_('Kanal'))
    body = models.TextField(verbose_name=_('Xabar matni'))
    is_read = models.BooleanField(default=False, verbose_name=_('O‘qilgan'))
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yuborilgan vaqti'))

    class Meta:
        verbose_name = _('Bildirishnoma')
        verbose_name_plural = _('Bildirishnomalar')
        ordering = ['-sent_at']

    def __str__(self):
        return f"Notification to {self.user} [{self.channel}]: {self.body[:40]}"
