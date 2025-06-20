from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm

from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from market.models import Provider
from market.models.intercoop import Intercoop
from django import forms

class IntercoopForm(MultiLangForm, BootstrapForm):

    class Meta:
        model = Intercoop
        widgets = {
            'node': forms.HiddenInput(),
            'description': CKEditorWidget(attrs={'cols': 190, 'rows': 5}),
        }
        exclude = ['created_at']

    def __init__(self, node, **kwargs):
        super().__init__(**kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(node=node)