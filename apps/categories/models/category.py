from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Kategoriya nomi'))
    slug = models.SlugField(max_length=120, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Ota kategoriya')
    )
    icon = models.CharField(max_length=50, default='fas fa-th-large', blank=True, verbose_name=_('Ikonka klassi'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Tartib raqami'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _('Kategoriyalar')
        ordering = ['order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    @property
    def is_root(self):
        return self.parent is None
