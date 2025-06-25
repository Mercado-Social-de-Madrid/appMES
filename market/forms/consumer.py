from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Consumer


class ConsumerForm(AccountForm):
    class Meta(AccountForm.Meta):
        model = Consumer
        exclude = AccountForm.Meta.exclude + ['idcard_file', 'idcard_file2', 'newsletter_check']

class CreateConsumerForm(CreateAccountFormMixin, ConsumerForm):
    pass
