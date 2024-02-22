from django import forms

from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Provider


class ProviderForm(AccountForm):

    class Meta(AccountForm.Meta):
        model = Provider

class CreateProviderForm(CreateAccountFormMixin, ProviderForm):
    pass