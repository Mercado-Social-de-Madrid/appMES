import os

from django.conf import settings
from rest_framework import serializers

from api.serializers.social_profile import SocialProfileSerializer
from core.models import Node


class NodeSerializer(serializers.ModelSerializer):
    social_profiles = SocialProfileSerializer(many=True, read_only=True)
    banner_image = serializers.StringRelatedField(source="banner_image.name")
    balance_badge = serializers.StringRelatedField(source="balance_badge.name")

    class Meta:
        model = Node
        exclude = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['info_page_url']:
            data['info_page_url'] = os.path.join(settings.BASESITE_URL, str(instance.id), "info")
        if not data['register_consumer_url']:
            data['register_consumer_url'] = f"{settings.BASESITE_URL}/consumer_register/{instance.shortname}"

        return data
