from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Qoralama')
        MODERATION = 'MODERATION', _('Moderatsiyada')
        ACTIVE = 'ACTIVE', _('Faol')
        REJECTED = 'REJECTED', _('Rad etilgan')
        ARCHIVED = 'ARCHIVED', _('Arxivlangan')
        SOLD = 'SOLD', _('Sotilgan')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('E‘lon egasi')
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('Kategoriya')
    )
    title = models.CharField(max_length=200, db_index=True, verbose_name=_('Sarlavha'))
    description = models.TextField(verbose_name=_('Tavsif'))
    price = models.DecimalField(max_digits=14, decimal_places=2, db_index=True, verbose_name=_('Narx (UZS)'))
    old_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, verbose_name=_('Eski narx (chizilgan narx, UZS)'))
    
    # Aksiya (Promotions & Discounts)
    is_promotion = models.BooleanField(default=False, db_index=True, verbose_name=_('Aksiya (Aksiya belgisi)'))
    promotion_text = models.CharField(max_length=50, default='AKSIYA', blank=True, verbose_name=_('Aksiya matni'))
    
    # Location coordinates for interactive map (Leaflet.js / OpenStreetMap)
    lat = models.FloatField(null=True, blank=True, verbose_name=_('Kenglik (Latitude)'))
    lng = models.FloatField(null=True, blank=True, verbose_name=_('Uzunlik (Longitude)'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('Shahar / Tuman'))
    address = models.CharField(max_length=255, blank=True, verbose_name=_('Aniq manzil'))

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.MODERATION,
        db_index=True,
        verbose_name=_('Holat')
    )
    reject_reason = models.TextField(blank=True, null=True, verbose_name=_('Rad etish sababi'))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Ko‘rishlar soni'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Yaratilgan vaqti'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yangilangan vaqti'))

    class Meta:
        verbose_name = _('E‘lon')
        verbose_name_plural = _('E‘lonlar')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} UZS ({self.get_status_display()})"

    @property
    def formatted_price(self):
        try:
            val = int(round(float(self.price)))
            return f"{val:,}".replace(",", " ")
        except (ValueError, TypeError):
            return f"{self.price}"

    @property
    def formatted_old_price(self):
        if not self.old_price:
            return ""
        try:
            val = int(round(float(self.old_price)))
            return f"{val:,}".replace(",", " ")
        except (ValueError, TypeError):
            return f"{self.old_price}"

    @property
    def primary_image_url(self):
        first_img = self.images.order_by('position', 'id').first()
        if first_img and first_img.image:
            return first_img.image.url
        elif first_img and first_img.url:
            return first_img.url
        return '/static/images/no-image.svg'
