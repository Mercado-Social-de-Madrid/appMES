from django.urls import reverse, resolve

from core.models import Node


class MarketMixin(object):
    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(pk=self.kwargs['market']).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.node:
            context['current_market'] = self.node

        return context

    def reverse(self, viewname, **kwargs):
        if not 'kwargs' in kwargs:
            kwargs['kwargs'] = {}
        kwargs['kwargs']['market'] = self.node.pk
        return reverse(viewname, **kwargs)