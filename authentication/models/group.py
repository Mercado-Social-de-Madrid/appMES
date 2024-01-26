from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext as _


class Group(DjangoGroup):
    class Meta:
        verbose_name = _('Grupo')
        verbose_name_plural = _('Grupos')
        proxy = True
