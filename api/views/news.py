from django.db.models import Q
from rest_framework import viewsets

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.news import NewsSerializer
from news.models import News


class NewsViewSet(FilterByNodeMixin, viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filterset_fields = ['published_by']
    search_fields = ['title', 'short_description', 'description']
