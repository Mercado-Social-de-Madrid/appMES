from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES

from helpers.filters.SemanticSearchFilter import SemanticSearchFilter
from django.utils.translation import gettext_lazy as _

class CommaSeparatedFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs


class ProviderFilter(FilterSet):
    categories__in = CommaSeparatedFilter(field_name="categories", lookup_expr="in")

    search = SemanticSearchFilter(
        names=['name', 'address', 'description', 'short_description', 'services'],
        vector_field='embedding_description',
        label=_('Búsqueda semántica...'))