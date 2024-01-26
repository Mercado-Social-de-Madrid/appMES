from rest_framework import viewsets

from api.serializers.node import NodeSerializer
from core.models import Node


class NodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
