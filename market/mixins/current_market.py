from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse, resolve

from core.models import Node
from market.models import Account


class MarketMixin(AccessMixin):
    node = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        user = self.request.user
        if 'market' in self.kwargs:
            self.node = Node.objects.filter(pk=self.kwargs['market']).first()
        elif user.is_staff:
            self.node = user.node
        else:
            account = user.accounts_managed.first()
            if account:
                self.node = account.node

    def dispatch(self, request, *args, **kwargs):
        if not self.user_can_access():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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

    def user_can_access(self):
        user = self.request.user
        if user.is_superuser:
            return True
        elif user.is_staff:
            # If is staff user, can access everything in the market she manages
            return self.node == user.node
        else:
            # If it's an average user, check if its in the current market
            account = user.accounts_managed.first()
            if account.node != self.node:
                return False
            # Custom check per-view based on user and the specific resource
            return self.user_can_access_resource(user)

    def user_can_access_resource(self, user):
        return False


class AccountAccessMixin(object):
    def user_can_access_resource(self, user):
        account = self.get_object()
        return user == account.owner

class OwnedByAccountAccessMixin(object):
    def user_can_access_resource(self, user):
        if not 'pk' in self.kwargs:
            return False

        account = Account.objects.get(pk=self.kwargs.get('pk'))
        return user == account.owner