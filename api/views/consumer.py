from django.http import HttpResponseForbidden
from rest_framework import authentication, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.consumer import ConsumerSerializer
from market.models import Consumer


class ConsumerViewSet(FilterByNodeMixin, RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        consumer = Consumer.objects.get(owner=request.user)
        serializer = ConsumerSerializer(consumer, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return HttpResponseForbidden('{"message":"Esta funcionalidad está desactivada temporalmente"}')
