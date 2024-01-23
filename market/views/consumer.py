from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView

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
        return super().get_queryset().filter(market=self.market)


class CreateConsumer(MarketMixin, CreateView):
    template_name = 'consumer/create.html'
    model = Provider
    form_class = ConsumerForm

    def get_initial(self):
        return { 'market': self.market }

    def get_success_url(self):
        messages.success(self.request, _('Consumidora añadida correctamente.'))
        return self.reverse('market:consumer_list')
