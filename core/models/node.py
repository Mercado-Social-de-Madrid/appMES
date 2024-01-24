from django.db import models
from django.utils.translation import gettext as _


class Node(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Nombre'))
    shortname = models.CharField(max_length=10)
    visible = models.BooleanField(default=False, verbose_name=_('Visible en listado público'), help_text=_('Por defecto, un nuevo mercado empieza oculto hasta que esté listo para incluir en la aplicación'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    class Meta:
        verbose_name = _('Mercado')
        verbose_name_plural = _('Mercados')