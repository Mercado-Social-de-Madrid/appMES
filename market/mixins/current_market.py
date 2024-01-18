from django.urls import reverse, resolve

from core.models import Market


class MarketMixin(object):
    market = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.market = Market.objects.filter(pk=self.kwargs['market']).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.market:
            context['current_market'] = self.market

        return context

    def reverse(self, viewname, **kwargs):
        if not 'kwargs' in kwargs:
            kwargs['kwargs'] = {}
        kwargs['kwargs']['market'] = self.market.pk
        return reverse(viewname, **kwargs)