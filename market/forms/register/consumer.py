
from market.forms.register.signup import BaseSignupForm
from market.forms.consumer import ConsumerForm


class ConsumerSignupForm(BaseSignupForm, ConsumerForm):
    required_fields = ['first_name', 'last_name']
