# coding=utf-8

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.template import loader

from helpers import mailing
from helpers.forms.BootstrapForm import BootstrapForm


class PasswordForm(BootstrapForm, PasswordChangeForm):
    pass


class FirstPasswordForm(BootstrapForm, SetPasswordForm):
    pass


class PasswordReset(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        title = loader.render_to_string(subject_template_name, context)

        mailing.send_template_email(
            title=title,
            destination=to_email,
            template_name='password_reset',
            template_params=context,
        )
