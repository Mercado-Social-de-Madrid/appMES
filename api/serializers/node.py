import os

from django.conf import settings
from rest_framework import serializers

from api.serializers.social_profile import SocialProfileSerializer
from core.models import Node


class NodeSerializer(serializers.ModelSerializer):
    social_profiles = SocialProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        exclude = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['info_page_url'] is None:
            data['info_page_url'] = os.path.join(settings.BASESITE_URL, str(instance.id), "info")

        return data
