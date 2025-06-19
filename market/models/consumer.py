
from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers import RandomFileName
from market.models import Account


class Consumer(Account):
    first_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Apellidos'))
    favorites = models.ManyToManyField("Provider", blank=True, verbose_name=_("Favoritos"))

    idcard_file = models.FileField(null=True, blank=True, verbose_name=_('Documento identificativo (DNI/NIE/Pasaporte...)'), upload_to=RandomFileName('dnis/'))
    idcard_file2 = models.FileField(null=True, blank=True, verbose_name=_('Documento identificativo (reverso)'), help_text=_('En caso de que hayas subido una foto con únicamente la parte delantera de tu documento, puedes subir aquí la trasera'), upload_to=RandomFileName('dnis/'))
    newsletter_check = models.BooleanField(default=False, verbose_name=_('Boletín de difusión'), help_text=_('Aceptas recibir el boletín informativo cono noticias y ventajas/ofertas para socias en formato electrónico'))

    is_intercoop = models.BooleanField(default=False, verbose_name=_('Es socia de intercooperación'))
    intercoop = models.ForeignKey("Intercoop", null=True, blank=True, verbose_name=_('Intercooperación'), on_delete=models.SET_NULL)
    intercoop_external_id = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Identificador de socia externa'))

    class Meta:
        verbose_name = _('Consumidora')
        verbose_name_plural = _('Consumidoras')
        ordering = ['-registration_date']

    @property
    def template_prefix(self):
        return 'consumer'

    @property
    def detail_url(self):
        return 'market:detail_consumer'

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

