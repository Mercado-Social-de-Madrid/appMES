from django import forms

from market.forms.account import AccountForm
from market.forms.register.signup import BaseSignupForm
from market.forms.consumer import ConsumerForm
from django.utils.translation import gettext_lazy as _


class ConsumerSignupForm(BaseSignupForm, ConsumerForm):
    required_fields = ['first_name', 'last_name', 'idcard_file']
    is_intercoop = forms.BooleanField(label=_('Quiero ser socia de intercooperación'), required=False, help_text=_('Si participas en alguna entidad con la que tenemos un acuerdo de intercooperación, puedes ser socia sin hacer el aporte inicial'))
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

