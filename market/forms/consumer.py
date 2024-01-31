from market.forms.account import AccountForm
from market.models import Consumer


class ConsumerForm(AccountForm):
    class Meta(AccountForm.Meta):
        model = Consumer



