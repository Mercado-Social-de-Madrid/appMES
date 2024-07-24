from django import forms

from helpers.forms.MultiLangForm import MultiLangForm
from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Provider
from ckeditor.widgets import CKEditorWidget


class ProviderForm(MultiLangForm, AccountForm):

    class Meta(AccountForm.Meta):
        model = Provider
        widgets = AccountForm.Meta.widgets | {
            'description': CKEditorWidget(attrs={'cols': 190, 'rows': 30}),
        }

class CreateProviderForm(CreateAccountFormMixin, ProviderForm):
    pass