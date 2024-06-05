# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from authentication.models import User
from helpers import send_template_email
from market.models import Account

logger = logging.getLogger(__name__)

class PreRegisteredUser(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=False, related_name='preregister', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, verbose_name=_('Cuenta'), on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False, verbose_name=_('Email preregistro enviado'))

    class Meta:
        verbose_name = _('Prerregistro')
        verbose_name_plural = _('Prerregistros')
        ordering = ['user']

    def send_email(self):
        if self.account:
            template = self.account.template_prefix + '_preregister'
        else:
            template = 'user' + '_preregister'

        title = _('Todo listo para empezar a usar la aplicación móvil del Mercado Social')

        try:
            logger.info("Enviando email de bienvenida de pre-registro")
            send_template_email(
                title=title,
                destination=self.user.email,
                template_name=template,
                template_params={
                    'token': self.id,
                    'user': self.user,
                    'account': self.account }
            )

            self.email_sent = True
            self.save()

            if self.account.node.admin_email:
                logger.info("Enviando confirmación de email de bienvenida a admin")
                send_template_email(
                    title=_('Nueva usuaria creada en la app'),
                    destination=self.account.node.admin_email,
                    template_name='admin_preregister_confirm_msg',
                    template_params={
                        'user': self.user,
                        'account': self.account }
                )

        except Exception as e:
            logger.error(f"Error al enviar email de bienvenida: {str(e)}")

    @staticmethod
    def create(account):
        PreRegisteredUser.objects.create(
            account=account,
            user=account.owner,
        )

    @staticmethod
    def create_user_and_preregister(account):
        if not account.owner:
            account.owner = User.objects.create_user(email=account.email, first_name=account.display_name, is_active=True)
            account.save()

        PreRegisteredUser.create(account)

    def __srt__(self):
        return '{} ({})'.format(self.user, self.id)


# When the preregister user is created, a preregister email is sent
@receiver(post_save, sender=PreRegisteredUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        instance.send_email()
