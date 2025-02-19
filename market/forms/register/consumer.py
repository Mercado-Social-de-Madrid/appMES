from django import forms

from market.forms.register.signup import BaseSignupForm
from market.forms.consumer import ConsumerForm


class ConsumerSignupForm(BaseSignupForm, ConsumerForm):
    required_fields = ['first_name', 'last_name', 'idcard_file']

    class Meta(ConsumerForm.Meta):
        widgets = {
             'idcard_file': forms.FileInput(attrs={'class': 'custom-file-input', }),
        }


