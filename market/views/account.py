import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from authentication.models.preregister import PreRegisteredUser
from authentication.views import CreateUser
from core.forms.address import AddressForm
from market.mixins.current_market import MarketMixin
from market.models import Account

_logger = logging.getLogger(__name__)


class AccountAddressMixin:
    """
    Manages the Account.address OneToOne relation with a separate, prefixed AddressForm
    """
    address_prefix = 'address'

    def get_address_form(self):
        account = getattr(self, 'object', None)
        instance = account.address if account else None
        return AddressForm(self.request.POST or None, instance=instance, prefix=self.address_prefix)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('address_form', self.get_address_form())
        return context

    def form_valid(self, form):
        address_form = self.get_address_form()
        if not address_form.is_valid():
            return self.form_invalid(form)

        response = super().form_valid(form)
        # Only save the address once the account (and its formsets) have been saved successfully
        if isinstance(response, HttpResponseRedirect) and (address_form.instance.pk or address_form.has_changed()):
            self.object.address = address_form.save()
            self.object.save(update_fields=['address'])
        return response


class UserAccountDetail(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        account = Account.objects.filter(owner=self.request.user).first()
        return reverse(account.detail_url, kwargs={'market':account.node.pk, 'pk': account.pk })


class UserAccountSocialBalance(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        account = Account.objects.filter(owner=self.request.user).first()
        return reverse('market:provider_balance', kwargs={'market':account.node.pk, 'pk': account.pk })


class ManageAccountUser(MarketMixin, CreateUser):
    template_name = 'account/add_user.html'
    account = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.account = Account.objects.get(pk=self.kwargs.get('pk'))

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'node': self.node, 'preferred_locale': self.node.preferred_locale })
        initial['email'] = self.account.email
        initial['first_name'] = self.account.display_name
        return initial

    # Redirect to user detail if the account already has one
    def get(self, request, *args, **kwargs):
        if self.account.owner is not None:
            user_detail_url = reverse('auth:user_detail', kwargs={'market':self.account.node.pk, 'pk': self.account.owner.pk })
            return HttpResponseRedirect(user_detail_url)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object:
            self.account.owner = self.object
            self.account.save()
            PreRegisteredUser.create(self.account)

        return response

    def get_success_url(self):
        messages.success(self.request, _('Usuario creado correctamente.'))
        return self.reverse('auth:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = self.account
        return context