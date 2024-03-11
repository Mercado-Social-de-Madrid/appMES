from rest_framework import serializers

from core.models.social_profile import SocialProfile


class SocialProfileSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="social_network.name")
    logo = serializers.StringRelatedField(source="social_network.logo_png.name")

    class Meta:
        model = SocialProfile
        fields = ['name', 'url', 'logo']


