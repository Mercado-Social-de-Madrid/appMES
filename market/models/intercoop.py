from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from market.models import Account, Provider
from django.utils.translation import gettext_lazy as _
from core.models import Gallery, Node
from market.models import Category
from pgvector.django import VectorField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.vectorize import vectorize_records

class Intercoop(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    created_at = models.DateField(verbose_name=_('Fecha de creación'), null=True, blank=True, auto_now_add=True)
    provider = models.OneToOneField(Provider, null=True, verbose_name=_('Entidad proveedora de intercooperación'), on_delete=models.SET_NULL)
    name = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Condiciones de intercooperación'))
    external_id_needed = models.BooleanField(default=True, verbose_name=_('Incluir identificador de socia externa para validación'))
    external_id_label = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Etiqueta del identificador en el formulario'))

    class Meta:
        verbose_name = _('Proveedora de intercooperación')
        verbose_name_plural = _('Proveedoras de intercooperación')
        ordering = ['name']

    @property
    def display_name(self):
        return self.provider.name if self.provider else self.name

    def __str__(self):
        return self.display_name