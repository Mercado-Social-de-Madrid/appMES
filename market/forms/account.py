from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Account
from django.utils.translation import gettext as _


class AccountForm(forms.ModelForm, BootstrapForm):

    class Meta:
        abstract = True
        model = Account
        widgets = {
            'node': forms.HiddenInput(),
            'profile_image': forms.FileInput(),
            'address': forms.Textarea(attrs={'rows': 3, }),
        }
        exclude = ['owner']

class CreateAccountFormMixin(forms.Form):

    create_preregister = forms.BooleanField(required=False, initial=True, label=_('Crear usuaria y mandar email de prerregistro'))
