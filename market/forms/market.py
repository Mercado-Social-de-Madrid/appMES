
from django import forms
from django.conf import settings

from core.models import Node
from helpers.forms.BootstrapForm import BootstrapForm


class MarketForm(forms.ModelForm, BootstrapForm):
    enabled_langs = forms.MultipleChoiceField(
        choices=settings.LANGUAGES,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Node
        widgets = {
            'register_consumer_url': forms.TextInput(),
            'register_provider_url': forms.TextInput(),
            'info_page_url': forms.TextInput(),
            'banner_image': forms.FileInput(),
            'balance_badge': forms.FileInput(),
            'preferred_locale': forms.Select(choices=settings.LANGUAGES)

        }
        exclude = ["takahe_server", "takahe_invite_url"]
