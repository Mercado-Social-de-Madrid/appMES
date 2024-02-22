from market.forms.account import AccountForm, CreateAccountFormMixin
from market.models import Consumer


class ConsumerForm(AccountForm):
    class Meta(AccountForm.Meta):
        model = Consumer


class CreateConsumerForm(CreateAccountFormMixin, ConsumerForm):
    pass
