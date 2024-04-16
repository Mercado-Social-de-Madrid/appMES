from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView

from authentication.models.preregister import PreRegisteredUser
from authentication.views import MarketCreateUser
from market.models import Account


class UserAccountDetail(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        account = Account.objects.filter(owner=self.request.user).first()
        return reverse(account.detail_url, kwargs={'market':account.node.pk, 'pk': account.pk })


class UserAccountSocialBalance(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        account = Account.objects.filter(owner=self.request.user).first()
        return reverse('market:provider_balance', kwargs={'market':account.node.pk, 'pk': account.pk })


class ManageAccountUser(MarketCreateUser):
    template_name = 'account/add_user.html'
    account = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.account = Account.objects.get(pk=self.kwargs.get('pk'))

    def get_initial(self):
        initial = super().get_initial()
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = self.account
        return context