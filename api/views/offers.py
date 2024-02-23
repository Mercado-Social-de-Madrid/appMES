from rest_framework import viewsets

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.offers import OffersSerializer
from offers.models import Offer


class OffersViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    search_fields = ['title', 'description']
