# coding=utf-8

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from helpers.forms.BootstrapForm import BootstrapForm


class PasswordForm(BootstrapForm, PasswordChangeForm):
    pass


class FirstPasswordForm(BootstrapForm, SetPasswordForm):
    pass
