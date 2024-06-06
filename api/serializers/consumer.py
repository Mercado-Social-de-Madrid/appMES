from rest_framework import serializers
from market.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    cif = serializers.ReadOnlyField()
    node = serializers.ReadOnlyField(source='node.pk')
    member_id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.pk')
    is_active = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()
    registration_date = serializers.ReadOnlyField()

    class Meta:
        model = Consumer
        exclude = ["polymorphic_ctype"]
