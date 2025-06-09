from rest_framework import serializers

from market.models import Provider


class ProviderSimpleSerializer(serializers.ModelSerializer):
    profile_image = serializers.StringRelatedField(source="profile_image.name")

    class Meta:
        model = Provider
        fields = ['id', 'name', 'profile_image', 'webpage_link']
