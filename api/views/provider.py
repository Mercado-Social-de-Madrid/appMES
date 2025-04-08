from django.http import HttpResponseGone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
#from rest_framework.filters import SemanticSearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from api.filters.provider import ProviderFilter
from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.provider import ProviderSerializer, ProviderGeoJsonSerializer
from market.models import Provider
from rest_framework import authentication, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProviderViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    search_fields = ['name', 'description', 'short_description', 'email']
    filter_backends = [DjangoFilterBackend, SearchFilter]#, SemanticSearchFilter]
    filterset_class = ProviderFilter


class ProviderAuthViewSet(FilterByNodeMixin, RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        provider = Provider.objects.get(owner=request.user)
        serializer = ProviderSerializer(provider, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EntitiesView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        return HttpResponseGone('{"message":"Es necesario actualizar la aplicación"}')




class ProviderGeoJsonViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderGeoJsonSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"type": "FeatureCollection", "features": serializer.data})
