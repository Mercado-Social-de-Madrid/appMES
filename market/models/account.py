import datetime
import uuid
from django.db import models, transaction
from polymorphic.models import PolymorphicModel
from imagekit.models import ProcessedImageField
from django.utils.translation import gettext_lazy as _
from pilkit.processors import ResizeToFill

from helpers import RandomFileName
from core.models import Node, Address
from authentication.models import User

MEMBER_ID_FORMAT = "{:05d}"


class Account(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Gestionado por'), related_name='accounts_managed')
    is_active = models.BooleanField(default=True, verbose_name=_('Activa'))
    cif = models.CharField(max_length=30, null=False, blank=False, verbose_name=_('NIF/CIF/Pasaporte'))
    email = models.CharField(null=False, blank=False, verbose_name='Email', max_length=250)
    phone_number = models.CharField(null=True, blank=True, verbose_name=_('Teléfono'), max_length=25)
    member_id = models.CharField(null=True, blank=True, max_length=20, verbose_name=_('Número de socia'))

    old_address = models.TextField(null=True, blank=True, verbose_name=_('Dirección (antigua)'))
    old_city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))

    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('profiles/'),
                               verbose_name='Imagen de perfil',
                               processors=[ResizeToFill(512, 512, upscale=False)], format='JPEG',
                               options={'quality': 90})

    address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='account', verbose_name=_('Dirección'))

    last_updated = models.DateTimeField(verbose_name=_('Última actualización'), null=True, blank=True)
    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True, default=datetime.date.today)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.member_id and not self.node.has_linked_crm:
            with transaction.atomic():
                self.member_id = Account.generate_member_id(self.node)
                return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)


    @staticmethod
    def generate_member_id(node):
        """
        Returns the next free member id of the node, and stores it as the node's last_member_id.
        Must be called inside a transaction: the node row stays locked until it ends
        """
        locked_node = Node.objects.select_for_update().get(pk=node.pk)
        number = locked_node.last_member_id
        while True:
            number += 1
            member_id = MEMBER_ID_FORMAT.format(number)
            # Skip numbers already taken (manually entered, or set while the node used an external CRM)
            if not Account.objects.filter(node=node, member_id=member_id).exists():
                break

        Node.objects.filter(pk=node.pk).update(last_member_id=number)
        node.last_member_id = number
        return member_id

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
