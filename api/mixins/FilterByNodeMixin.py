from django.core.exceptions import FieldError
from django.db.models import Q


class FilterByNodeMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        node = self.kwargs.get("node")

        possible_fields = ['node', 'provider__node', 'entity__node']

        for field in possible_fields:
            try:
                queryset = queryset.filter(Q(**{field: node}))
                break
            except FieldError:
                pass

        return queryset
