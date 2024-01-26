from rest_framework import viewsets

from api.serializers.category import CategorySerializer
from market.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
