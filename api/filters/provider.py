from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES


class CommaSeparatedFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs


class ProviderFilter(FilterSet):
    categories__in = CommaSeparatedFilter(field_name="categories", lookup_expr="in")
