from django.db import models
from django.db.models import Q

from core.models.time_stamped_model import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Address(TimeStampedModel):
    address = models.CharField(null=True, blank=True, max_length=500, verbose_name=_('Dirección'))
    city = models.ForeignKey("cities_light.City", null=True, blank=True, on_delete=models.SET_NULL, max_length=250, verbose_name=_('Municipio'))
    region = models.ForeignKey("cities_light.SubRegion", null=True, blank=True, on_delete=models.SET_NULL, max_length=250, verbose_name=_('Provincia'))
    postcode = models.CharField(null=True, blank=True, max_length=50, verbose_name=_("Código postal"))

    class Meta:
        verbose_name = _('Dirección')
        verbose_name_plural = _('Direcciones')

    @classmethod
    def create_from_text(cls, address=None, city_name=None):
        """
        Creates an Address from free-text values (legacy imports, API), trying to match the city by name.
        Returns None if there is nothing to store.
        """
        from cities_light.models import City

        city = None
        if city_name:
            city_name = city_name.strip()
            city = City.objects.filter(Q(name__iexact=city_name) | Q(name_ascii__iexact=city_name)).first()

        if not address and not city:
            return None

        return cls.objects.create(address=address, city=city, region=city.subregion if city else None)



    def __str__(self):
        city = self.city.name if self.city else None
        region = f"({self.region.name})" if self.region else None
        return ", ".join(part for part in [self.address, city, region] if part)
