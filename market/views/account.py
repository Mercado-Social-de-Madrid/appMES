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
from core.mixins.FormsetView import FormsetView
from market.models import Account

_logger = logging.getLogger(__name__)

class AccountFormSet(FormsetView):
    def get_named_formsets(self):
        return {
            'addresses': AddressForm.getAddressFormset(),
        }

    def formset_addresses_get_initial(self):
        initial_data = None
        account = None
        if self.object:
            initial_data = self.object.addresses
            account = self.object.id
        return AddressForm.get_initial(addresses=initial_data, account=account)

    def formset_addresses_valid(self, address_formset, account):
        _logger.debug(f"ADDRESS VALID. ACCOUNT: {account}")
        for address in account.addresses.all():
            _logger.debug(f"Deleting address: {address.address}")
            address.delete()

        _logger.debug(f"address_formset: {address_formset}")

        for address_form in address_formset:
            address = address_form.save(commit=False)
            if address_form.cleaned_data.get('DELETE'):
                continue

            _logger.debug(f"ADDRESS: {address}")
            address.account = account
            _logger.debug(f"ADDRESS.ACCOUNT: {address.account}")
            address.address = address_form.cleaned_data.get("address")
            address.city = address_form.cleaned_data.get("city")
            address.town = address_form.cleaned_data.get("town")
            address.postcode = address_form.cleaned_data.get("postcode")
            address.save()


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