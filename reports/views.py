# coding=utf-8
import datetime

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.views.generic import TemplateView

from benefits.models import Benefit
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from market.mixins.current_market import MarketMixin
from market.models import Provider
from offers.models import Offer

days_query = {
    'year': 365,
    '3month':90,
    'month': 30,
    'week': 7,
}


class OffersChartView(MarketMixin, AjaxTemplateResponseMixin, TemplateView):
    template_name = 'reports/offers_card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last = self.request.GET.get('last', 'month')
        days = days_query[last]
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        published = Offer.objects.published_last_days(days).filter(provider__node=self.node)

        context['last'] = last
        context['published'] = published
        context['active'] = Offer.objects.active_last_days(days)
        context['providers'] = Provider.objects.filter(node=self.node, pk__in=published.values_list('provider').distinct())
        context['daily'] = published.annotate(day=TruncDay('published_date')).values('day').annotate(total=Count('id')).order_by('day')
        context['date_ranges'] = { 'start': since, 'end': today }
        return context


class BenefitsChartView(MarketMixin, AjaxTemplateResponseMixin, TemplateView):
    template_name = 'reports/benefits_card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last = self.request.GET.get('last', 'month')
        days = days_query[last]
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        published = Benefit.objects.filter(published_date__gte=since, entity__node=self.node)

        context['last'] = last
        context['published'] = published.count()
        context['total'] = Benefit.objects.filter(entity__node=self.node).count()
        context['num_providers'] = Provider.objects.filter(node=self.node).count()
        return context

