from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Category, Provider


class ProviderForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Provider
        widgets = {
            'market': forms.HiddenInput(),
        }
        exclude = []

