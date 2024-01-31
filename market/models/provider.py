from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from market.models import Account
from django.utils.translation import gettext as _
from core.models import Gallery
from market.models import Category


class Provider(Account):

    name = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    short_description = models.TextField(null=True, blank=True, verbose_name=_('Descripción corta'))

    not_listed = models.BooleanField(default=False, verbose_name=_('Oculta en listado público'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('Categorías'))

    phone_number = models.CharField(null=True, blank=True, verbose_name=_('Teléfono'), max_length=25)
    num_workers = models.IntegerField(default=0, verbose_name=_('Número de trabajadores'), validators=[MinValueValidator(0)])
    legal_form = models.TextField(null=True, blank=True, verbose_name=_('Formulario legal'))

    gallery = models.OneToOneField(Gallery, blank=True, null=True, on_delete=models.SET_NULL)

    balance_detail = models.CharField(null=True, blank=True, verbose_name=_('Informe balance'), max_length=250)

    # Social links
    facebook_link = models.CharField(null=True, blank=True, verbose_name=_('Página de Facebook'), max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name=_('Página web'), max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name=_('Perfil de X'), max_length=250)
    telegram_link = models.CharField(null=True, blank=True, verbose_name=_('Canal de Telegram'), max_length=250)
    instagram_link = models.CharField(null=True, blank=True, verbose_name=_('Perfil de Instagram'), max_length=250)
    fediverse_link = models.CharField(null=True, blank=True, verbose_name=_('Perfil en Fediverso'), max_length=250)

    class Meta:
        verbose_name = 'Proveedora'
        verbose_name_plural = 'Proveedoras'
        ordering = ['name']

    @property
    def balance_url(self):
        return settings.BASESITE_URL + "/balance/" + self.member_id if self.member_id and self.balance_detail else None

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
                return image.image.url
        return None

    @property
    def qr_code(self):
        return settings.BASESITE_URL + reverse('entity_qr_detail',  kwargs={'pk': self.pk} )
