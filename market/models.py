import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from polymorphic.models import PolymorphicModel

from core.models import Market, Gallery
from helpers import RandomFileName


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    color = models.CharField(null=True, blank=True, verbose_name='Color de etiqueta (código hexadecimal)', max_length=30)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name if self.name else ''

    def __unicode__(self):
        return self.name if self.name else ''



class Account(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=_('Gestionado por'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activa'))
    cif = models.CharField(max_length=30, null=False, blank=False, verbose_name=_('NIF/CIF/Pasaporte'))
    email = models.CharField(null=False, blank=False, verbose_name='Email', max_length=250)
    member_id = models.CharField(null=True, blank=True, max_length=20, verbose_name=_('Número de socia'))
    address = models.TextField(null=True, blank=True, verbose_name=_('Dirección'))
    city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))

    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('profiles/'),
                               verbose_name='Imagen de perfil',
                               processors=[ResizeToFill(512, 512, upscale=False)], format='JPEG',
                               options={'quality': 90})

    last_updated = models.DateTimeField(verbose_name=_('Última actualización'), null=True, blank=True)
    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True)

    @property
    def template_prefix(self):
        return 'account'

    @property
    def detail_url(self):
        return 'accounts:provider_detail'

    @property
    def display_name(self):
        return self.cif

    def __str__(self):
        return self.display_name



class Provider(Account):

    name = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    short_description = models.TextField(null=True, blank=True, verbose_name=_('Descripción corta'))

    not_listed = models.BooleanField(default=False, verbose_name=_('Oculta en listado público'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('Categorías'))

    phone_number = models.CharField(null=True, blank=True, verbose_name=_('Teléfono'), max_length=25)
    num_workers = models.IntegerField(default=0, verbose_name=_('Número de trabajadores'), validators = [MinValueValidator(0)])
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
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        ordering = ['name']

    @property
    def balance_url(self):
        return settings.BASESITE_URL + "/balance/" + self.member_id if self.member_id and self.balance_detail else None

    @property
    def display_name(self):
        return self.name

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


class Consumer(Account):
    first_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Apellidos'))
    favorites = models.ManyToManyField(Provider, blank=True, verbose_name=_("Favoritos"))
    is_intercoop = models.BooleanField(default=False, verbose_name=_('Es socia de intercooperación'))

    class Meta:
        verbose_name = _('Consumidora')
        verbose_name_plural = _('Consumidoras')

    @property
    def template_prefix(self):
        return 'consumer'

    @property
    def detail_url(self):
        return 'accounts:consumer_detail'

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

