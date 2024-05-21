from django.http import HttpResponseGone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.provider import ProviderSerializer
from market.models import Provider
from market.views import ProviderFilter


class ProviderViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    search_fields = ['name', 'description', 'short_description', 'email']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProviderFilter


class EntitiesView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        return HttpResponseGone('{"message":"Es necesario actualizar la aplicación"}')

