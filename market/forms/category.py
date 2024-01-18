from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Category


class CategoryForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Category
        widgets = {
            'market': forms.HiddenInput(),
            'color': forms.TextInput(attrs={'class': 'color-widget'}),
        }
        exclude = []

