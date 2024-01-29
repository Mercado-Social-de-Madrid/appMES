from rest_framework import viewsets

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.category import CategorySerializer
from market.models import Category


class CategoryViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['node']
    search_fields = ['name', 'description']
