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

class EditMarket(UpdateView):
    template_name = 'market/edit.html'
    form_class = MarketForm
    model = Market

class MarketDashboard(MarketMixin, TemplateView):
    template_name = 'dashboard/market.html'