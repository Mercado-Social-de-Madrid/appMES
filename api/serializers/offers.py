from rest_framework import serializers

from api.serializers.provider_simple import ProviderSimpleSerializer
from offers.models import Offer


class OffersSerializer(serializers.ModelSerializer):
    banner_image = serializers.StringRelatedField(source="banner_image.name")
    provider = ProviderSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = Offer
        exclude = []


