from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Message(models.Model):
    chat = models.ForeignKey(
        'chats.Chat',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Chat')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Yuboruvchi')
    )
    body = models.TextField(verbose_name=_('Xabar matni'))
    is_read = models.BooleanField(default=False, verbose_name=_('O‘qilgan'))
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yuborilgan vaqti'))

    class Meta:
        verbose_name = _('Xabar')
        verbose_name_plural = _('Xabarlar')
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
