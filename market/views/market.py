from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from core.models import Market
from market.forms.market import MarketForm
from market.mixins.current_market import MarketMixin


class MarketList(ListView):
    template_name = 'market/list.html'
    model = Market

class AddMarket(CreateView):
    template_name = 'market/create.html'
    form_class = MarketForm
    model = Market

    def get_success_url(self):
        return reverse('market:market_list', )

class EditMarket(UpdateView):
    template_name = 'market/edit.html'
    form_class = MarketForm
    model = Market

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return reverse('market:edit_market', kwargs={"pk": self.object.pk})

class MarketDashboard(MarketMixin, TemplateView):
    template_name = 'dashboard/market.html'