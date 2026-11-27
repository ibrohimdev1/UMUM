from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTPVerification(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'OTP Tasdiqlash'
        verbose_name_plural = 'OTP Tasdiqlashlar'
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at and self.attempts < 3

    @classmethod
    def generate_otp(cls, phone, code, validity_minutes=2):
        expires_at = timezone.now() + timedelta(minutes=validity_minutes)
        return cls.objects.create(phone=phone, code=code, expires_at=expires_at)
