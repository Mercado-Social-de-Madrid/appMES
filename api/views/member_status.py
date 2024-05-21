from django.http import HttpResponseNotFound
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from market.models import Consumer, Provider


class MemberStatusViewSet(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        city = request.GET["city"]
        member_id = request.GET["member_id"]

        response = {
            'city': city,
        }

        member = Consumer.objects.filter(node__shortname__iexact=city, member_id=member_id).first()
        if member is not None:
            response['member_type'] = 'person'
            response['is_intercoop'] = member.is_intercoop
        else:
            member = Provider.objects.filter(node__shortname__iexact=city, member_id=member_id).first()
            if member is None:
                return HttpResponseNotFound()
            response['member_type'] = 'entity'

        response['is_active'] = member.is_active
        return Response(response)

