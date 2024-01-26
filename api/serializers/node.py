from rest_framework import serializers

from core.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = []
