from django import forms

from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Provider
from ckeditor.widgets import CKEditorWidget


class ProviderForm(AccountForm):

    class Meta(AccountForm.Meta):
        model = Provider
        widgets = AccountForm.Meta.widgets | {
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
        }

class CreateProviderForm(CreateAccountFormMixin, ProviderForm):
    pass