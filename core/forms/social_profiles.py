import logging

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _

from core.models.social_profile import SocialNetwork, ProviderSocialProfile, SocialProfile, NodeSocialProfile
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.widgets.SocialNetworkWidget import SocialNetworkWidget

logger = logging.getLogger(__name__)


class SocialProfileForm(forms.ModelForm, BootstrapForm):
    social_network = forms.ModelChoiceField(queryset=SocialNetwork.objects.all(), widget=SocialNetworkWidget)
    url = forms.CharField(max_length=100, required=False, widget=forms.widgets.TextInput(attrs={'placeholder': _('Enlace a la red social.')}))

    class Meta:
        model = SocialProfile
        fields = ['social_network', 'url']

    def clean_url(self):
        url = self.cleaned_data['url']
        if url:
            if '://' not in url:
                url = 'https://' + url

            validator = URLValidator()
            try:
                validator(url)
            except ValidationError:
                logger.error("La URL no es válida.")
                raise forms.ValidationError(_("Introduce una URL válida."))

        return url

    @staticmethod
    def get_initial(initial_social_profiles=None):
        social_networks = SocialNetwork.objects.all()

        social_profiles_data = []
        for social_network in social_networks:
            url = None
            if initial_social_profiles and initial_social_profiles.filter(social_network=social_network).exists():
                url = initial_social_profiles.get(social_network=social_network).url

            social_profiles_data.append({
                'social_network': social_network,
                'url': url
            })

        return social_profiles_data


class ProviderSocialProfileForm(SocialProfileForm):
    class Meta:
        model = ProviderSocialProfile
        fields = ['social_network', 'url']

    @staticmethod
    def getSocialProfileFormset():
        return formset_factory(form=ProviderSocialProfileForm, extra=0)


class NodeSocialProfileForm(SocialProfileForm):
    class Meta:
        model = NodeSocialProfile
        fields = ['social_network', 'url']

    @staticmethod
    def getSocialProfileFormset():
        return formset_factory(form=NodeSocialProfileForm, extra=0)
