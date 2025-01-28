from django.contrib import messages
from django.db.models import Q

from authentication.models.preregister import PreRegisteredUser
from authentication.views.user import UserList, CreateUser, UpdateUser
from market.mixins.current_market import MarketMixin
from django.utils.translation import gettext_lazy as _

class MarketUserList(MarketMixin, UserList):
    def get_queryset(self):
        return super().get_queryset().filter(Q(node=self.node) | Q(accounts_managed__node=self.node))


class MarketCreateUser(MarketMixin, CreateUser):
    def get_initial(self):
        initial = super().get_initial() or {}
        initial.update({'node': self.node, 'preferred_locale': self.node.preferred_locale })
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        # Creating the preregistered user sends the welcome email
        PreRegisteredUser.objects.create(user=self.object)
        return response

    def get_success_url(self):
        messages.success(self.request, _('Usuario creado correctamente.'))
        return self.reverse('auth:user_list')


class MarketUpdateUser(MarketMixin, UpdateUser):
    def get_queryset(self):
        return super().get_queryset().filter(Q(node=self.node) | Q(accounts_managed__node=self.node))

    def get_success_url(self):
        return self.reverse('auth:user_list')