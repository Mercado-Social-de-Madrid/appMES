from rest_framework import serializers

from offers.models import Offer


class OffersSerializer(serializers.ModelSerializer):
    banner_image = serializers.StringRelatedField(source="banner_image.name")

    class Meta:
        model = Offer
        exclude = []


