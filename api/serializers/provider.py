from rest_framework import serializers

from api.serializers.social_profile import SocialProfileSerializer
from market.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    social_profiles = SocialProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        exclude = []
