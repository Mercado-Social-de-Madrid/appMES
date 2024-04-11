from django.urls import reverse, resolve

from core.models import Node


class MarketMixin(object):
    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(pk=self.kwargs['market']).first()
        elif not self.request.user.is_staff:
            account = self.request.user.accounts_managed.first()
            if account:
                self.node = account.node

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.node:
            context['current_market'] = self.node

        return context

    def reverse(self, viewname, **kwargs):
        if not 'kwargs' in kwargs:
            kwargs['kwargs'] = {}
        if self.node:
            kwargs['kwargs']['market'] = self.node.pk
        return reverse(viewname, **kwargs)