from rest_framework import viewsets

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.benefits import BenefitsSerializer
from benefits.models import Benefit


class BenefitsViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitsSerializer
    search_fields = ['benefit_for_entities', 'benefit_for_members']
