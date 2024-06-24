from rest_framework import serializers

from api.serializers.account import AccountSerializer
from market.models import Consumer


class ConsumerSerializer(AccountSerializer):

    name = serializers.StringRelatedField(source='first_name')
    surname = serializers.StringRelatedField(source='last_name')
    nif = serializers.ReadOnlyField(source='cif')
    profile_image = serializers.StringRelatedField(source='profile_image.name')
    profile_thumbnail = serializers.StringRelatedField(source='profile_image.name')

    class Meta:
        model = Consumer
        exclude = ["polymorphic_ctype"]

