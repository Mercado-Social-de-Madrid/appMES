import logging

from django.http import HttpResponseBadRequest
from rest_framework import authentication
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins.FilterByNodeMixin import FilterByNodeMixin
from api.serializers.account import ProfileImageSerializer
from market.models import Account

logger = logging.getLogger(__name__)


class ProfileImageViewSet(FilterByNodeMixin, UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        account = Account.objects.get(owner=request.user)
        serializer = ProfileImageSerializer(account, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

        logger.error("Error al actualizar la imagen de perfil:")
        logger.error(serializer.errors)
        return HttpResponseBadRequest('{"message":"Ha habido un error al actualizar la imagen de perfil"}')
