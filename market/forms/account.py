from django import forms
from django.utils.translation import gettext as _

from authentication.models import User
from helpers.forms.BootstrapForm import BootstrapForm
from market.models import Account


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

    def clean(self):
        cleaned_data = super().clean()
        preregister = cleaned_data.get('create_preregister')
        email = cleaned_data.get('email')

        if preregister and email:
        # If the user should be created, we need to check if no user exists already with that email
            if User.objects.filter(email=email).exists():
                self.add_error('email', _('Ya existe un usuario registrado con este email.'))

        return cleaned_data