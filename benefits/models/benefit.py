from django.db import models
from django.utils.translation import gettext as _
from market.models import Provider


class Benefit(models.Model):
    entity = models.OneToOneField(Provider, null=False, blank=False, related_name='benefit', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    benefit_for_entities = models.TextField(null=True, blank=True, verbose_name=_('Ventajas para entidades'))
    benefit_for_members = models.TextField(null=True, blank=True, verbose_name=_('Ventajas para socias'))
    includes_intercoop_members = models.BooleanField(default=False, null=False, verbose_name=_('Incluye socias Intercoop'))
    in_person = models.BooleanField(default=True, null=False, verbose_name=_('Solicitud física'))
    online = models.BooleanField(default=True, null=False, verbose_name=_('Solicitud online'))
    discount_code = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Código de descuento'))
    discount_link_entities = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Link de descuento para entidades'))
    discount_link_members = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Link de descuento para socias'))
    discount_link_text = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Texto del botón del link de descuento'), default=_("Solicitar descuento"))
    active = models.BooleanField(default=True, null=False, verbose_name=_('Activa'))

    class Meta:
        verbose_name = 'Ventaja'
        verbose_name_plural = 'Ventajas'
        ordering = ['-published_date']

    @property
    def can_edit(self, user):
        return user.is_staff