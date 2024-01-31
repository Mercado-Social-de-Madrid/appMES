from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from market.forms.consumer import ConsumerForm
from market.mixins.current_market import MarketMixin
from market.models import Provider, Consumer


class ConsumerList(MarketMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'consumer/list.html'
    model = Consumer
    objects_url_name = 'consumer_detail'
    ajax_template_name = 'consumer/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class CreateConsumer(MarketMixin, CreateView):
    template_name = 'consumer/create.html'
    model = Consumer
    form_class = ConsumerForm

    def get_initial(self):
        return { 'node': self.node }

    def get_success_url(self):
        messages.success(self.request, _('Consumidora añadida correctamente.'))
        return self.reverse('market:consumer_list')

    def form_invalid(self, form):
        return super().form_invalid(form)

class ConsumerDetail(MarketMixin, DetailView):
    model = Consumer
    template_name = 'consumer/detail.html'


class ConsumerEdit(MarketMixin, UpdateView):
    model = Consumer
    form_class = ConsumerForm
    template_name = 'consumer/edit.html'

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return self.reverse('market:detail_consumer', kwargs={'pk':self.object.pk})