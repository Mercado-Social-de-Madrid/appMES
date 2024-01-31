from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from market.mixins.current_market import MarketMixin


# Create your views here.
class HomeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return reverse('market:admin_dashboard')
        elif self.request.user.is_staff:
            return reverse('market:market_dashboard', kwargs={ 'market': self.request.user.node.pk })
        else:
            return reverse('market:user_dashboard')


class AdminDashboard(TemplateView):
    template_name = 'dashboard/admin.html'

class MarketDashboard(MarketMixin, TemplateView):
    template_name = 'dashboard/market.html'


class UserDashboard(TemplateView):
    template_name = 'dashboard/user.html'
