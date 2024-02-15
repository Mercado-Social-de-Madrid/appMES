from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from helpers import RandomFileName


class Node(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Nombre'))
    shortname = models.CharField(max_length=10)
    visible = models.BooleanField(default=False, verbose_name=_('Visible en listado público'), help_text=_('Por defecto, un nuevo mercado empieza oculto hasta que esté listo para incluir en la aplicación'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    contact_email = models.EmailField(null=True, blank=True, max_length=200, verbose_name=_('Email de contacto'))
    self_register_allowed = models.BooleanField(default=False, verbose_name=_('Permitir el registro abierto'))
    register_provider_url = models.TextField(blank=True, null=True, verbose_name=_('Enlace al formulario de registro de proveedoras'))
    register_consumer_url = models.TextField(blank=True, null=True, verbose_name=_('Enlace al formulario de registro de consumidoras'))
    preferred_locale = models.CharField(max_length=10, default='es-ES', verbose_name=_('Idioma preferido de la interfaz'))
    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('node/'),
                                       verbose_name=_('Imagen principal'),
                                       processors=[ResizeToFit(756, 512, upscale=False)], format='JPEG')
    takahe_server = models.URLField(blank=True, null=True, verbose_name=_('Servidor de Takahe'))

    class Meta:
        verbose_name = _('Mercado')
        verbose_name_plural = _('Mercados')

    def __str__(self):
        return self.name