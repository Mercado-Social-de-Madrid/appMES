import os

from django.db import models

from core.models.time_stamped_model import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Address(TimeStampedModel):
    account = models.ForeignKey("market.Account", null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Cuenta'), related_name='addresses')
    address = models.CharField(null=True, blank=True, max_length=500, verbose_name=_('Dirección'))
    town = models.ForeignKey("cities_light.City", null=True, blank=True, on_delete=models.DO_NOTHING, max_length=250, verbose_name=_('Municipio'))
    city = models.ForeignKey("cities_light.SubRegion", null=True, blank=True, on_delete=models.DO_NOTHING, max_length=250, verbose_name=_('Provincia'))
    postcode = models.CharField(null=True, blank=True, max_length=50, verbose_name=_("Código postal"))

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.address}, {self.town}, {self.postcode}, ({self.city})"
