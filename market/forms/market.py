
from django import forms
from core.models import Node
from helpers.forms.BootstrapForm import BootstrapForm


class MarketForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Node
        widgets = {
            'register_consumer_url': forms.TextInput(),
            'register_provider_url': forms.TextInput(),
            'info_page_url': forms.TextInput(),
            'banner_image': forms.FileInput()
        }
        exclude = []
