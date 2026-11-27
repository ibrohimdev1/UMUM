from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('Telefon raqami kiritilishi shart!'))
        phone = phone.strip().replace(' ', '')
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('status', User.Status.ACTIVE)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser is_staff=True bo‘lishi kerak.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser is_superuser=True bo‘lishi kerak.'))

        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER = 'USER', _('Foydalanuvchi')
        ADMIN = 'ADMIN', _('Administrator')

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Faol')
        BLOCKED = 'BLOCKED', _('Bloklangan')

    phone = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=_('Telefon'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    full_name = models.CharField(max_length=150, blank=True, verbose_name=_('To‘liq ism'))
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER, verbose_name=_('Rol'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, verbose_name=_('Holat'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('Shahar'))
    seller_profile_completed = models.BooleanField(default=False, verbose_name=_('Sotuvchi profili to‘ldirilgan'))
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_('Profil rasmi'))

    is_staff = models.BooleanField(default=False, verbose_name=_('Admin xodimi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktiv'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name = _('Foydalanuvchilar')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name or self.phone} ({self.phone})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
