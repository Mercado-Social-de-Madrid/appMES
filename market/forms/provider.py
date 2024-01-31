from django import forms

from market.forms.account import AccountForm
from market.models import Provider


class ProviderForm(AccountForm):

    class Meta(AccountForm.Meta):
        model = Provider

