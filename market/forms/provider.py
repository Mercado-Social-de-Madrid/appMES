from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Category, Provider


class ProviderForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Provider
        widgets = {
            'node': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': 3, }),
            'latitude': forms.NumberInput(attrs={'readonly': True}),
            'longitude': forms.NumberInput(attrs={'readonly': True}),
        }
        exclude = ['owner']

