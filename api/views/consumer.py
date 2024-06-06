import logging

from django.http import HttpResponseBadRequest
from rest_framework import authentication, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.consumer import ConsumerSerializer
from market.models import Consumer

logger = logging.getLogger(__name__)


class ConsumerViewSet(FilterByNodeMixin, RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        consumer = Consumer.objects.get(owner=request.user)
        serializer = ConsumerSerializer(consumer, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        consumer = Consumer.objects.get(owner=request.user)
        consumer_serializer = ConsumerSerializer(consumer, data=data)
        if consumer_serializer.is_valid():
            consumer_serializer.save()
            return Response(data=consumer_serializer.data)

        logger.error("Error al editar perfil de consumidora:")
        logger.error(consumer_serializer.errors)
        return HttpResponseBadRequest('{"message":"Ha habido un error al editar el perfil"}')
