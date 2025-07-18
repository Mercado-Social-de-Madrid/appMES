from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit
from django.contrib.postgres.fields import ArrayField

from helpers import RandomFileName


class Node(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Nombre'))
    shortname = models.CharField(max_length=10)
    visible = models.BooleanField(default=False, verbose_name=_('Visible en listado público'), help_text=_('Por defecto, un nuevo mercado empieza oculto hasta que esté listo para incluir en la aplicación'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    contact_email = models.EmailField(null=True, blank=True, max_length=200, verbose_name=_('Email de contacto'))
    admin_email = models.EmailField(null=True, blank=True, max_length=200, verbose_name=_('Email de administración'), help_text=_('Para mensajes de la herramienta'))
    self_register_allowed = models.BooleanField(default=False, verbose_name=_('Permitir el registro abierto'))
    register_provider_url = models.TextField(blank=True, null=True, verbose_name=_('Enlace al formulario de registro de proveedoras'))
    register_consumer_url = models.TextField(blank=True, null=True, verbose_name=_('Enlace al formulario de registro de consumidoras'))

    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('node/'),
                                       verbose_name=_('Imagen principal'),
                                       processors=[ResizeToFit(756, 512, upscale=False)], format='PNG')
    balance_badge = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('badge/'),
                                       verbose_name=_('Imagen del distintivo de balance'),
                                       processors=[ResizeToFit(512, 512, upscale=False)], format='PNG')

    webpage_link = models.URLField(blank=True, null=True, verbose_name=_('Página web'), max_length=250)
    takahe_server = models.URLField(blank=True, null=True, verbose_name=_('Servidor de Takahe'))
    takahe_invite_url = models.URLField(blank=True, null=True, verbose_name=_('Enlace de invitación a Takahe'))

    has_linked_crm = models.BooleanField(default=False, verbose_name=_('Utiliza herramienta de gestión para las socias'))
    linked_crm_url = models.URLField(blank=True, null=True, verbose_name=_('URL del servidor de la Herramienta de gestión'))
    member_card_enabled = models.BooleanField(default=True, verbose_name=_('Carnet de socia activa'))
    info_page_url = models.TextField(blank=True, null=True, verbose_name=_('Enlace a página con información básica del mercado'))

    preferred_locale = models.CharField(max_length=10, default='es-ES', verbose_name=_('Idioma preferido de la interfaz'))
    enabled_langs = ArrayField(models.CharField(max_length=3, choices=settings.LANGUAGES), blank=True, default=[], verbose_name=_('Idiomas habilitados'))

    privacy_policy_url = models.URLField(blank=True, null=True, verbose_name=_('Enlace a la política de privacidad'))
    intercoop_enabled = models.BooleanField(default=False, verbose_name=_('Habilitar funcionalidad de intercooperación'))

    @property
    def is_multilang_enabled(self):
        return len(self.enabled_langs) > 1

    class Meta:
        verbose_name = _('Mercado')
        verbose_name_plural = _('Mercados')

    def __str__(self):
        return self.name