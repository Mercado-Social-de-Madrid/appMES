import uuid
from django.db import models
from polymorphic.models import PolymorphicModel
from imagekit.models import ProcessedImageField
from django.utils.translation import gettext as _
from pilkit.processors import ResizeToFill

from helpers import RandomFileName
from core.models import Node
from authentication.models import User


class Account(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Gestionado por'), related_name='accounts_managed')
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
        return self.cif
