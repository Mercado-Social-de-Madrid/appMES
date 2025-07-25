import logging
from http import HTTPStatus

from django.http import HttpResponse, Http404

from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from core.models import Node

from django.utils.translation import gettext_lazy as _, activate

from helpers import send_template_email
from market.forms.register.consumer import ConsumerSignupForm
from market.models import Intercoop

logger = logging.getLogger(__name__)

class RegisterView(XFrameOptionsExemptMixin, CreateView):
    template_name = 'consumer/register/form.html'
    form_class = ConsumerSignupForm

    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            market = self.kwargs['market']
            try:
                self.node = Node.objects.filter(pk=int(market)).first()
            except ValueError:
                self.node = Node.objects.filter(shortname=market).first()
            if not self.node:
                raise Http404("")
            activate(self.node.preferred_locale)

    def dispatch(self, *args, **kwargs):
        if self.node.self_register_allowed and not self.node.register_consumer_url:
            return super().dispatch(*args, **kwargs)
        else:
            return HttpResponse(_("El registro interno no está disponible para este mercado."), status=HTTPStatus.FORBIDDEN)

    def get_initial(self):
        initial = super().get_initial() or {}
        initial.update({'node': self.node})
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.node
        context["privacy_policy_url"] = self.node.privacy_policy_url
        if self.node.intercoop_enabled:
            context['intercoop_entities'] = Intercoop.objects.filter(node=self.node)
        return context

    def form_invalid(self, form):
        logger.error(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        self.send_email_to_admins(self.object)
        self.send_email_to_consumer(self.object)

        messages.success(self.request, _('Consumidora añadida correctamente.'))
        return response

    def get_success_url(self):
        success_url = reverse('market:consumer_register_success', kwargs=self.kwargs)

        from_app = self.request.GET.__contains__("from_app")
        if from_app:
            return success_url + "?from_app"

        hide_toolbar = self.request.GET.__contains__("hide_toolbar")
        if hide_toolbar:
            return success_url + "?hide_toolbar"

        return success_url

    def send_email_to_admins(self, consumer):
        try:
            logger.info("Enviando confirmación de email de bienvenida a admin")
            send_template_email(
                title=_('Nueva solicitud de socia consumidora'),
                destination=consumer.node.admin_email,
                template_name='admin_consumer_preregister_request',
                template_params={ 'consumer': consumer, 'node':consumer.node }
            )
        except Exception as e:
            logger.error(e)

    def send_email_to_consumer(self, consumer):
        try:
            logger.info("Enviando confirmación de email de bienvenida a socia consumidora")
            send_template_email(
                title=_("Solicitud de alta en el Mercado Social de {node}").format(node=consumer.node.name),
                destination=consumer.email,
                template_name='consumer_preregister_request',
                template_params={
                    'account': consumer,
                    'node': consumer.node,
                }
            )
        except Exception as e:
            logger.error(e)

class RegisterDoneView(XFrameOptionsExemptMixin, TemplateView):
    template_name = "consumer/register/success.html"
    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(shortname=self.kwargs['market']).first()
            activate(self.node.preferred_locale)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.node
        context['contact_mail'] = self.node.contact_email
        return context
