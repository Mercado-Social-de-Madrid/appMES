from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from market.models import Category


class CategoryForm(MultiLangForm, BootstrapForm, forms.ModelForm):

    class Meta:
        model = Category
        widgets = {
            'node': forms.HiddenInput(),
            'color': forms.TextInput(attrs={'class': 'color-widget'}),
        }
        exclude = []

