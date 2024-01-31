from rest_framework import viewsets

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.provider import ProviderSerializer
from market.models import Provider


class ProviderViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filterset_fields = ['node']