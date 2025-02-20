from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Consumer


class ConsumerForm(AccountForm):
    class Meta(AccountForm.Meta):
        model = Consumer
        exclude = AccountForm.Meta.exclude + ['idcard_file', 'newsletter_check']

class CreateConsumerForm(CreateAccountFormMixin, ConsumerForm):
    pass
