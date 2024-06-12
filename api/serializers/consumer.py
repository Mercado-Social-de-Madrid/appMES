from rest_framework import serializers

from api.serializers.account import AccountSerializer
from market.models import Consumer


class ConsumerSerializer(AccountSerializer):

    name = serializers.CharField(source='first_name')
    surname = serializers.CharField(source='last_name')
    nif = serializers.CharField(source='cif')
    profile_thumbnail = serializers.CharField(source='profile_image')

    class Meta:
        model = Consumer
        exclude = ["polymorphic_ctype"]
