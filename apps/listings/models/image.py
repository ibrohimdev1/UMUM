from django.db import models
from django.utils.translation import gettext_lazy as _

class ListingImage(models.Model):
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('E‘lon')
    )
    image = models.ImageField(upload_to='listings/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Rasm fayli'))
    url = models.CharField(max_length=500, blank=True, verbose_name=_('Tashqi havola'))
    position = models.PositiveSmallIntegerField(default=0, verbose_name=_('Tartibi'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('E‘lon rasmi')
        verbose_name_plural = _('E‘lon rasmlari')
        ordering = ['position', 'id']

    def __str__(self):
        return f"Image for {self.listing.title} (#{self.position})"

    @property
    def file_url(self):
        if self.image:
            return self.image.url
        return self.url or '/static/images/no-image.svg'
