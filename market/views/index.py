from django.shortcuts import render
from django.views.generic import TemplateView

from market.mixins.current_market import MarketMixin


# Create your views here.
class HomeView(MarketMixin, TemplateView):
    template_name = 'index.html'
