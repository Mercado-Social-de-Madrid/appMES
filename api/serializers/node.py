from rest_framework import serializers

from api.serializers.social_profile import SocialProfileSerializer
from core.models import Node


class NodeSerializer(serializers.ModelSerializer):
    social_profiles = SocialProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        exclude = []
