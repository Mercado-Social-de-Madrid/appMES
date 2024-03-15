import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from core.models import Node
from core.models.time_stamped_model import TimeStampedModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)


class User(TimeStampedModel, AbstractUser):
    username = None
    email = models.EmailField(_('Correo Electrónico'), unique=True)
    first_name = models.CharField(_('Nombre'), max_length=150, validators=[MinLengthValidator(3)], null=False, blank=False)
    last_name = models.CharField(_('Apellidos'), max_length=150, null=True, blank=True)
    node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Mercado que gestiona'))
    manages_multi = models.BooleanField(default=False, verbose_name=_('Maneja entidades en más de un mercado'))
    preferred_locale = models.CharField(default='es-ES', max_length=10, verbose_name=_('Idioma preferido de la interfaz'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

        permissions = (
            ("mespermission_can_manage_users", _("Puede ver la lista de usuarios")),
            ("mespermission_can_change_passwords", _("Puede cambiar la contraseña de un usuario")),
            ("mespermission_can_view_user_history", _("Puede consultar el historial de un usuario")),
            ("mespermission_can_update_users", _("Puede modificar usuarios")),
            ("mespermission_can_view_user_detail", _("Puede ver los detalles de un usuario")),
            ("mespermission_can_create_users", _("Puede añadir usuarios")),

        )

    def __str__(self):
        return self.email

    def is_preregistered(self):
        return self.preregister.all().count() > 0

    @property
    def display_name(self):
        return self.first_name or self.email
