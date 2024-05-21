from rest_framework import serializers
from market.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        exclude = ["polymorphic_ctype"]
