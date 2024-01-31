from django import forms

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
