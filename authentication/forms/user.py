# coding=utf-8
import datetime
from django import forms
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm

from authentication.models import User
from core.models import Node
from helpers.forms.BootstrapForm import BootstrapForm
from django.utils.translation import gettext_lazy as _

class UserForm(BootstrapForm, forms.ModelForm):
    node = forms.ModelChoiceField(queryset=Node.objects.all(), required=True, label=_('Mercado que gestiona'))

    class Meta:
        model = User
        fields = ['first_name', 'node', 'email', 'preferred_locale', 'manages_multi', 'is_staff']
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'disabled': True}),
            'first_name': forms.TextInput(attrs={'placeholder': _('Nombre')}),
            'preferred_locale': forms.Select(choices=settings.LANGUAGES),
        }

class ProfileForm(BootstrapForm, forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = ['email', 'preferred_locale']
        widgets = { 'preferred_locale': forms.Select(choices=settings.LANGUAGES)}


class PasswordForm(BootstrapForm, SetPasswordForm):
    pass

