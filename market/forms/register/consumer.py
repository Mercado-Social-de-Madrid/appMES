from django import forms

from market.forms.account import AccountForm
from market.forms.register.signup import BaseSignupForm
from market.forms.consumer import ConsumerForm
from django.utils.translation import gettext_lazy as _

from market.models import Intercoop


class ConsumerSignupForm(BaseSignupForm, ConsumerForm):
    required_fields = ['first_name', 'last_name', 'idcard_file']
    is_intercoop = forms.BooleanField(label=_('Quiero ser socia de intercooperación'), required=False, help_text=_('Ingresar como socia/o de intercooperación a través de mi condición de socia en:'))
    class Meta(ConsumerForm.Meta):
        widgets = ConsumerForm.Meta.widgets | {
            'idcard_file': forms.FileInput(attrs={'class': 'custom-file-input', }),
            'idcard_file2': forms.FileInput(attrs={'class': 'custom-file-input', }),
        }
        exclude = AccountForm.Meta.exclude


    def clean(self):
        cleaned_data = super().clean()

        is_intercoop = cleaned_data.get('is_intercoop', False)
        if is_intercoop:
            intercoop = cleaned_data.get('intercoop')
            if not intercoop:
                self.add_error("is_intercoop", _('Tienes que seleccionar una entidad de intercooperación concreta'))
                return

            intercoop_external_id = cleaned_data.get('intercoop_external_id')
            if intercoop.external_id_needed and intercoop_external_id in ("", None):
                self.add_error("intercoop_external_id", _('Este campo no puede estar vacío.'))
