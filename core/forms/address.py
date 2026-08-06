from django.conf import settings
from django import forms
from django.forms import formset_factory

from modeltranslation.utils import get_language
from core.models import Address
from helpers.forms.BootstrapForm import BootstrapForm
from django.utils.translation import gettext_lazy as _
from cities_light.models import SubRegion, City
import logging

_logger = logging.getLogger(__name__)

def translate_cities():
    lang = get_language()
    short_lang = lang.split('-')[0] if lang else settings.MODELTRANSLATION_DEFAULT_LANGUAGE
    cities = SubRegion.objects.all().values('id', 'name', 'translations', 'region')
    translated_cities = []
    for city in cities:
        id = city.get("id")
        name = city.get("name")
        translations = city.get("translations")
        try:
            translated_city = (id, translations[short_lang][0])
        except KeyError:
            translated_city = (id, name)
        translated_cities.append(translated_city)

    return translated_cities

class AddressForm(forms.ModelForm, BootstrapForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].choices = [translated_city for translated_city in translate_cities()]

        city_field_name = self.add_prefix('city')

        try:
            if self.initial and "city" in self.initial:
                self.fields['town'].queryset = City.objects.filter(subregion_id=self.initial.get('city').id).order_by('name')
            else:
                if self.data and city_field_name in self.data:
                    city_id = int(self.data.get(city_field_name))
                    self.fields['town'].queryset = City.objects.filter(subregion_id=city_id).order_by('name')
                else:
                    self.fields['town'].queryset = City.objects.none()

            self.fields['town'].choices = [(town.id, town.name) for town in self.fields['town'].queryset]
        except (ValueError, TypeError):
            pass

    class Meta:
        model = Address
        exclude = []
        widgets = {
            'account': forms.widgets.HiddenInput(),
            'city': forms.Select(attrs={'class':  'city-select'}),
            'town': forms.Select(attrs={'class': 'town-select'})
        }

    @staticmethod
    def getAddressFormset():
        return formset_factory(form=AddressForm, extra=0, max_num=1, min_num=1, can_delete=False)

    @staticmethod
    def get_initial(addresses=None, account=None):
        if addresses is None:
            return None

        if not addresses.all().exists():
            return [{ 'account': account }]

        addresses_data = []
        for address in addresses.all():
            address_data = {
                'account': account,
                'address': address.address,
                'city': address.city,
                'town': address.town,
                'postcode': address.postcode,
            }
            addresses_data.append(address_data)

        return addresses_data
