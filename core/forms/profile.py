# coding=utf-8
import datetime
from django import forms
from django.contrib.auth.models import User

from core.models import UserProfile
from helpers.forms.BootstrapForm import BootstrapForm


class UserForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', ]
        widgets = {
            'username': forms.TextInput(attrs={'readonly':True }),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_locale']
