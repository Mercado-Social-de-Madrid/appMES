import logging

from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from rest_framework import authentication, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.consumer import ConsumerSerializer
from api.serializers.provider import ProviderSerializer
from api.serializers.user import UserSerializer
from authentication.models import User
from authentication.models.api_token import APIToken
from authentication.models.preregister import PreRegisteredUser
from market.management.commands.import_madrid_data import set_social_profiles, set_categories
from market.models import Account, Provider, Consumer, Category
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class FetchUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):


        data = request.data

        instance = None
        if 'uuid' in data:
            instance = Account.objects.get(id=data['uuid'])
        if instance is None and 'cif' in data and data['cif'] is not None:
            try:
                instance = Account.objects.get(cif=data['cif'])
            except MultipleObjectsReturned:
                raise Exception(f"Duplicated person. CIF: {data['cif']}. ")
        if instance is None and 'email' in data and data['email'] is not None:
            try:
                instance = Account.objects.get(email=data['email'])
            except MultipleObjectsReturned:
                raise Exception(f"Duplicated person. Email: {data['email']}")
        if instance is None:
            return HttpResponseNotFound()

        if instance.node != request.user.node:
            return HttpResponseForbidden()

        response = {"api_key": APIToken.objects.get_or_create(user=instance.owner)[0].key}
        if isinstance(instance, Consumer):
            response['type'] = "person"
            response['person'] = ConsumerSerializer(instance).data
            if (response['person'] is not None) and 'owner' in response['person']:
                response['person']['id'] = instance.id
                del response["person"]["owner"]

                response['person']['profile_image'] = instance.profile_image.url if instance.profile_image else None

                if response['person']['favorites']:
                    for i, uuid in enumerate(response['person']['favorites']):
                        response['person']['favorites'][i] = uuid
        elif isinstance(instance, Provider):
            response['type'] = "entity"
            response['entity'] = ProviderSerializer(instance).data
            if (response['entity'] is not None) and 'user' in response['entity']:
                response['entity']['id'] = instance.id
                if response['entity']['logo']:
                    response['entity']['logo'] = instance.profile_image.url if instance.profile_image else None
                del response['entity']['user']
                del response['entity']['gallery']

                if instance.categories.count() > 0:
                    response['entity']['categories'] = []
                    for cat in instance.categories.all():
                        response['entity']['categories'].append(cat.pk)

        response['user'] = UserSerializer(instance.owner).data
        response['user']['is_registered'] = instance.owner.is_registered()

        return Response(data=response, status=status.HTTP_200_OK)


class PreRegisterUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        logger.info("Recibida petición de pre-registro")

        data = request.data

        account = None
        email = data['email']

        if not request.user.node:
            logger.info(f"Este usuario no gestiona ningún mercado: {request.user.email}")
            return HttpResponse(_("Este usuario no gestiona ningún mercado."), status=400)

        logger.info(f"Iniciando pre-registro para [{email}]")

        if User.objects.filter(email=email).exists():
            logger.warning("Ya existe un usuario registrado con este correo electrónico.")
            return HttpResponse(_("Ya existe un usuario registrado con este correo electrónico."), status=400)

        result = {}
        if 'person' in data:
            consumer = data['person']
            account = Consumer.objects.create(
                node=request.user.node,
                cif=consumer.get('cif'),
                email=email,
                member_id=consumer.get('member_id'),
                first_name=consumer.get('name'),
                last_name=consumer.get('surname'),
                address=consumer.get('address'),
                city=consumer.get('city'),
                phone_number=consumer.get('contact_phone'),
                is_intercoop=consumer.get('is_intercoop', False)
            )
            result = {"person": {"id": account.id}}
        elif 'entity' in data:
            provider = data['entity']
            account = Provider.objects.create(
                node=request.user.node,
                cif=provider.get('cif'),
                email=email,
                member_id=provider.get('member_id'),
                name=provider.get('name'),
                address=provider.get('address'),
                city=provider.get('city'),
                description=provider.get('description'),
                short_description=provider.get('short_description'),
                latitude=provider.get('latitude', 0),
                longitude=provider.get('longitude', 0),
                num_workers=provider.get('num_workers', 1),
                legal_form=provider.get('legal_form'),
                webpage_link=provider.get('webpage_link'),
                phone_number=provider.get('contact_phone'),
            )
            set_social_profiles(provider, account)
            set_categories(provider, account)

            result = {"entity": {"id": account.id}}
        else:
            logger.error("No existe objeto entity o person en el cuerpo de la petición")
            return HttpResponse(_("No existe objeto entity o person en el cuerpo de la petición"), status=400)

        PreRegisteredUser.create_user_and_preregister(account)
        logger.info("Usuario pre-registrado creado con exito.")
        return JsonResponse(result, status=200)
