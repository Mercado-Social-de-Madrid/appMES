from django.http import HttpResponseGone
from rest_framework import viewsets
from rest_framework.views import APIView

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.provider import ProviderSerializer
from market.models import Provider


class ProviderViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class EntitiesView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        return HttpResponseGone('{"message":"Es necesario actualizar la aplicación"}')

