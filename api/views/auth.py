import logging

from django.contrib.auth import get_user_model, logout, login
from rest_framework import generics, status, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from authentication.models.api_token import APIToken

logger = logging.getLogger(__name__)


User = get_user_model()


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            u = User.objects.get(email=request.data['username'])
            if not u.is_active:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={'error': _('Tu cuenta no está activa, revisa tu bandeja de entrada de correo.')}
                )
            else:
                raise e

        user = serializer.validated_data['user']
        token, created = APIToken.objects.get_or_create(user=user)
        login(request, user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'token': token.key,
                'user_id': user.pk,
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
        return Response(
            status=status.HTTP_200_OK,
            data={'response': _('Usuario eliminado con éxito.')}
        )

#
# class ResetPasswordView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         user_email = request.data['email']
#         logger.info(f"Starting reset password process for user [{user_email}]")
#         try:
#             user = User.objects.get(email=user_email)
#             reset_password_token, created = ResetPasswordToken.objects.update_or_create(user=user)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         email.send_email(user, email.RESET_PASSWORD_EMAIL, {"reset_password_token": reset_password_token.key})
#         return Response(status=status.HTTP_200_OK)
#
