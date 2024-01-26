from rest_framework import serializers

from market.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        exclude = []
