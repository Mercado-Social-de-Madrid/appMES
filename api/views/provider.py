from rest_framework import viewsets

from api.serializers.provider import ProviderSerializer
from market.models import Provider


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
