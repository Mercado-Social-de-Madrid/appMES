from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm

from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
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
