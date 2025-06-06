from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from market.models import Account
from django.utils.translation import gettext_lazy as _
from core.models import Gallery
from market.models import Category
from pgvector.django import VectorField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.vectorize import vectorize_records

class Provider(Account):

    name = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    short_description = models.TextField(null=True, blank=True, verbose_name=_('Descripción corta'))
    services = models.TextField(null=True, blank=True, verbose_name=_('Productos y servicios'))
    embedding_description = VectorField(dimensions=384, verbose_name=_('Descripción y productos vectorizados'), null=True, blank=True)

    not_listed = models.BooleanField(default=False, verbose_name=_('Oculta en listado público'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('Categorías'))

    num_workers = models.IntegerField(default=0, verbose_name=_('Número de trabajadores'), validators=[MinValueValidator(0)])
    legal_form = models.TextField(null=True, blank=True, verbose_name=_('Forma legal'))

    gallery = models.OneToOneField(Gallery, blank=True, null=True, on_delete=models.SET_NULL)

    balance_detail = models.CharField(null=True, blank=True, verbose_name=_('Informe balance'), max_length=250)

    webpage_link = models.CharField(null=True, blank=True, verbose_name=_('Página web'), max_length=250)


    class Meta:
        verbose_name = 'Proveedora'
        verbose_name_plural = 'Proveedoras'
        ordering = ['name']

    @property
    def balance_url(self):
        return f"{settings.BASESITE_URL}/{self.node.id}/balance/{self.member_id}" if self.member_id and self.balance_detail else None

    @property
    def display_name(self):
        return self.name

    @property
    def detail_url(self):
        return 'market:provider_detail'

    @property
    def template_prefix(self):
        return 'provider'

    @property
    def first_photo_url(self):
        if self.gallery and self.gallery.photos.count() > 0:
            image = self.gallery.photos.all().first()
            if image:
                return image.photo.url
        return None

    @property
    def qr_code(self):
        return settings.BASESITE_URL + reverse('entity_qr_detail',  kwargs={'pk': self.pk} )


@receiver(pre_save, sender=Provider)
def update_embedding(sender, instance, **kwargs):
    """
    Signal that is automatically executed when a record is inserted or updated in Provider.
    """
    vectorize_field = "services" if instance.services else "description"
    vectorize_records("market",
                      "Provider",
                      [vectorize_field],
                      "embedding_description",
                      instance=instance,
                      save=False)