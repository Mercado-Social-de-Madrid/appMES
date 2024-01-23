from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Category, Provider, Consumer


class ConsumerForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Consumer
        widgets = {
            'market': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': 3, }),
        }
        exclude = []

