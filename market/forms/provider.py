from django import forms

from helpers.forms.MultiLangForm import MultiLangForm
from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Provider
from ckeditor.widgets import CKEditorWidget


class ProviderForm(MultiLangForm, AccountForm):

    class Meta(AccountForm.Meta):

        model = Provider
        widgets = AccountForm.Meta.widgets | {
            'short_description': forms.widgets.Textarea(attrs={'cols': 190, 'rows': 2, 'maxlength': '320'}),
            'description': CKEditorWidget(attrs={'cols': 190, 'rows': 30}),
            'services': CKEditorWidget(attrs={'cols': 190, 'rows': 30}),
        }
        exclude = AccountForm.Meta.exclude + ['embedding_description']

class CreateProviderForm(CreateAccountFormMixin, ProviderForm):
    pass