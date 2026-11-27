from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AuditLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_actions',
        verbose_name=_('Amal bajaruvchi')
    )
    action = models.CharField(max_length=100, db_index=True, verbose_name=_('Harakat turi'))
    entity = models.CharField(max_length=100, db_index=True, verbose_name=_('Obyekt'))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP manzil'))
    extra_data = models.JSONField(default=dict, blank=True, verbose_name=_('Qo‘shimcha ma‘lumotlar'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Vaqti'))

    class Meta:
        verbose_name = _('Audit yozuvi')
        verbose_name_plural = _('Audit jurnali')
        ordering = ['-created_at']

    def __str__(self):
        actor_name = self.actor.phone if self.actor else "System"
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M')}] {actor_name} -> {self.action} ({self.entity})"
