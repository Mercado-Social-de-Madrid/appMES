import logging
from http import HTTPStatus

from django.http import HttpResponse

from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from authentication.forms.register.consumer import ConsumerSignupForm
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from core.models import Node

from django.utils.translation import gettext_lazy as _, activate

from helpers import send_template_email

logger = logging.getLogger(__name__)

class RegisterView(XFrameOptionsExemptMixin, CreateView):
    template_name = 'registration/register/consumer/register_consumer.html'
    form_class = ConsumerSignupForm

    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(shortname=self.kwargs['market']).first()
            activate(self.node.preferred_locale)

    def dispatch(self, *args, **kwargs):
        if self.node.self_register_allowed and self.node.register_consumer_url:
            return HttpResponse(_("El registro interno no está disponible para este mercado."), status=HTTPStatus.FORBIDDEN)
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial() or {}
        initial.update({'node': self.node})
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["privacy_policy_url"] = self.node.privacy_policy_url
        return context

    def form_invalid(self, form):
        logger.error(form.errors)
        return super(RegisterView,self).form_invalid(form)

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)

        self.send_email_to_admins(self.object)
        self.send_email_to_consumer(self.object)

        messages.success(self.request, _('Consumidora añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('auth:register_request_done', kwargs=self.kwargs)

    def send_email_to_admins(self, consumer):
        try:
            logger.info("Enviando confirmación de email de bienvenida a admin")
            send_template_email(
                title=_('Nueva solicitud de socia consumidora'),
                destination=consumer.node.admin_email,
                template_name='admin_consumer_preregister_request',
                template_params={'consumer': consumer}
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
    template_name = "registration/register/register_request_done.html"
    title = _("Registration email sent")

    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(shortname=self.kwargs['market']).first()
            activate(self.node.preferred_locale)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_mail'] = self.node.contact_email
        return context
