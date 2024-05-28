import json
import logging

from django.contrib.auth import get_user_model, logout, login
from rest_framework import generics, status, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from authentication.forms.password import PasswordReset
from authentication.models.api_token import APIToken
from market.models import Account, Provider

logger = logging.getLogger(__name__)

User = get_user_model()


def parse_account_data(account):
    return {
        'id': account.id,
        'member_id': account.member_id,
        'city': account.node.shortname,
        'email': account.email,
        'inactive': not account.is_active,
        'is_active': account.is_active,
        'address': account.address,
        'profile_image': account.profile_image.name,
        'profile_thumbnail': account.profile_image.name,
    }


def parse_entity_data(account):
    account_data = parse_account_data(account)
    return account_data | {
        'hidden': False,
        'cif': account.cif,
        'name': account.name,
    }


def parse_person_data(account):
    account_data = parse_account_data(account)
    return account_data | {
        'name': account.first_name,
        'surname': account.last_name,
        'is_guest_account': False,
        'is_intercoop': account.is_intercoop,
        'fav_entities': [],
        'nif': account.cif,
    }


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            u = User.objects.filter(email=request.data['username']).first()
            if not u:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={'error': _('Usuario no encontrado.')}
                )
            elif not u.is_active:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={'error': _('Tu cuenta no está activa, revisa tu bandeja de entrada de correo.')}
                )
            else:
                raise e

        user = serializer.validated_data['user']
        token, created = APIToken.objects.get_or_create(user=user)
        login(request, user)

        # RESPONSE RETROCOMPATIBLE, PENDING REFACTOR WHEN APPS ARE READY
        type = None
        entity = None
        person = None

        if user.is_superuser:
            type = 'superuser'
        elif user.is_staff:
            type = 'staff'
        else:
            account = Account.objects.get(owner=user)
            is_provider = isinstance(account, Provider)

            if is_provider:
                entity = parse_entity_data(account)
                type = 'entity'
            else:
                person = parse_person_data(account)
                type = 'person'

        data = {
            'api_key': token.key,
            'user_id': user.pk,
            'type': type,
            'entity': entity,
            'person': person,
        }

        return Response(
            status=status.HTTP_200_OK,
            data={
                'success': True,
                'data': data
            }
        )


class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        user = APIToken.objects.get(pk=request.user.auth_token).user
        user.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK, data={'response': _('Usuario eliminado con éxito.')})


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        logger.info(f"Starting reset password process for email [{email}]")
        try:
            User.objects.get(email=email)
            reset_form = PasswordReset(request.data)
            if reset_form.is_valid():
                reset_form.save()
                return Response(status=status.HTTP_200_OK, data={})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': json.dumps(reset_form.errors)})
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
