# coding=utf-8
import datetime
from django import forms
from authentication.models import User
from helpers.forms.BootstrapForm import BootstrapForm


class UserForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'node', 'last_name', 'email', 'preferred_locale', 'manages_multi', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'preferred_locale']
