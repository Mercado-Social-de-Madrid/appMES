
from django import forms
from django.conf import settings

from core.models import Node
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from django.utils.translation import gettext_lazy as _


class MarketForm(BootstrapForm, MultiLangForm, forms.ModelForm):

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["register_consumer_url"].widget.attrs.update(
                {'placeholder':  f'{settings.BASESITE_URL}/consumer_register/{self.instance.shortname}'}
            )

class MarketPublicForm(BootstrapForm, MultiLangForm, forms.ModelForm):

    class Meta:
        model = Node
        widgets = {
            'info_page_url': forms.TextInput(),
            'balance_badge': forms.FileInput(),
        }
        help_texts = {
            'info_page_url': _('Dejar en blanco para usar la página por defecto de la app'),
        }

        fields = ['info_page_url', 'contact_email', 'admin_email', 'privacy_policy_url', 'balance_badge', 'webpage_link']