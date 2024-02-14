from django.db.models import Q


class FilterByNodeMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        node = self.kwargs.get("node")
        if node:
            queryset = queryset.filter(Q(node__name__iexact=node) | Q(node__shortname__iexact=node))
        return queryset
