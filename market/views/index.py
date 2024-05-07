import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

import helpers
from market.mixins.current_market import MarketMixin
from market.models import Account, Provider, Consumer
from news.models import News
from offers.models import Offer


days_query = {
    'year': 365,
    '3month':90,
    'month': 30,
    'week': 7,
}

DASHBOARD_LIST_PAGECOUNT = 5

# Create your views here.
class HomeView(LoginRequiredMixin, RedirectView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['last_news'] = News.objects.filter(node=self.node).order_by('-published_date')[:3]
        last = self.request.GET.get('last', 'month')
        query = days_query[last]
        today = datetime.date.today()
        since = today - datetime.timedelta(days=query)
        context['last'] = last
        context['total_providers'] = Provider.objects.count()
        context['total_consumers'] = Consumer.objects.count()
        context['new_providers'] = helpers.paginate(
            Provider.objects.filter(node=self.node, registration_date__gte=since),
            1, elems_perpage=DASHBOARD_LIST_PAGECOUNT)
        context['new_consumers'] = helpers.paginate(
            Consumer.objects.filter(node=self.node, registration_date__gte=since),
            1, elems_perpage=DASHBOARD_LIST_PAGECOUNT)
        return context

class UserDashboard(LoginRequiredMixin, MarketMixin, TemplateView):
    template_name = 'dashboard/user.html'

    def get_account(self):
        return Account.objects.filter(owner=self.request.user).first()

    def get_template_names(self):
        account = self.get_account()
        if isinstance(account, Provider):
            return 'dashboard/provider.html'
        else:
            return 'dashboard/consumer.html'

    def user_can_access(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        account = self.get_account()
        context['account'] = account

        if isinstance(account, Provider):
            context['num_offers'] = Offer.objects.current(provider=account).count()

        context['last_news'] = News.objects.filter(node=account.node).order_by('-published_date')[:3]

        return context
