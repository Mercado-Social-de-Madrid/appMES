from django.conf import settings
from django import forms

from modeltranslation.utils import get_language
from core.models import Address
from helpers.forms.BootstrapForm import BootstrapForm
from cities_light.abstract_models import to_ascii
from cities_light.models import SubRegion, City


def translated_regions():
    lang = get_language()
    short_lang = lang.split('-')[0] if lang else settings.MODELTRANSLATION_DEFAULT_LANGUAGE
    regions = SubRegion.objects.order_by('name').values('id', 'name', 'translations')
    translated = []
    for region in regions:
        try:
            name = region.get('translations')[short_lang][0]
        except (KeyError, IndexError, TypeError):
            name = region.get('name')
        translated.append((region.get('id'), name))

    # Sort ignoring accents, so "Ávila" goes with the A's instead of at the end
    return sorted(translated, key=lambda region: to_ascii(region[1]).lower())


class AddressForm(forms.ModelForm, BootstrapForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].choices = [('', '---------')] + translated_regions()

        # The city options depend on the selected region (province)
        region_id = self.data.get(self.add_prefix('region')) if self.is_bound else self.initial.get('region')
        try:
            cities = City.objects.filter(subregion_id=int(region_id)).order_by('name')
        except (ValueError, TypeError):
            cities = City.objects.none()
        self.fields['city'].queryset = cities

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        region = cleaned_data.get('region')
        if city and region and city.subregion_id != region.id:
            self.add_error('city', forms.ValidationError(self.fields['city'].error_messages['invalid_choice'], code='invalid_choice'))
        return cleaned_data

    class Meta:
        model = Address
        fields = ['address', 'postcode', 'region', 'city']
        widgets = {
            'region': forms.Select(attrs={'class': 'region-select'}),
            'city': forms.Select(attrs={'class': 'city-select'}),
        }
