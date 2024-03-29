from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from market.mixins.current_market import MarketMixin
from market.models import Account, Provider
from news.models import News
from offers.models import Offer


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
        return context
class UserDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user.html'

    def get_account(self):
        return Account.objects.filter(owner=self.request.user).first()

    def get_template_names(self):
        account = self.get_account()
        if isinstance(account, Provider):
            return 'dashboard/provider.html'
        else:
            return 'dashboard/consumer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        account = self.get_account()
        context['account'] = account

        if isinstance(account, Provider):
            context['num_offers'] = Offer.objects.current(provider=account).count()

        context['last_news'] = News.objects.filter(node=account.node).order_by('-published_date')[:3]

        return context

class UserAccountDetail(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        account = Account.objects.filter(owner=self.request.user).first()
        return reverse(account.detail_url, kwargs={'market':account.node.pk, 'pk': account.pk })
