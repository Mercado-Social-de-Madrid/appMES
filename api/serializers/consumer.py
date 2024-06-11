

from api.serializers.account import AccountSerializer
from market.models import Consumer


class ConsumerSerializer(AccountSerializer):

    class Meta:
        model = Consumer
        exclude = ["polymorphic_ctype"]
