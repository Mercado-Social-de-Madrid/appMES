# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from authentication.models import User
from helpers import send_template_email
from market.models import Account


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
        except Exception as e:
            print(e)


    @staticmethod
    def create_user_and_preregister(account):
        if not account.owner:
            account.owner = User.objects.create_user(email=account.email, first_name=account.display_name, is_active=True)
            account.save()

        PreRegisteredUser.objects.create(
            account=account,
            user=account.owner,
        )

    def __srt__(self):
        return '{} ({})'.format(self.user, self.id)


# When the preregister user is created, a preregister email is sent
@receiver(post_save, sender=PreRegisteredUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        instance.send_email()
