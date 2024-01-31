from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.translation import gettext as _

from authentication.forms.password import PasswordForm
from authentication.forms.user import ProfileForm, UserForm
from authentication.models import User
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.mixins.current_market import MarketMixin


class UserList(ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'user/list.html'
    model = User
    objects_url_name = 'user_detail'
    ajax_template_name = 'user/query.html'
    paginate_by = 15

class UpdateUser(UpdateView):
    template_name = 'user/edit.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('auth:user_list')

class CreateUser(CreateView):
    template_name = 'user/add.html'
    model = User
    form_class = UserForm

    def get_success_url(self):
        messages.success(self.request, _('Usuario creado correctamente.'))
        return reverse('auth:user_list')


class MarketUserList(MarketMixin, UserList):
    def get_queryset(self):
        return super().get_queryset().filter(Q(node=self.node) | Q(accounts_managed__node=self.node))


class MarketCreateUser(MarketMixin, CreateUser):
    def get_initial(self):
        return { 'node': self.node }

    def get_success_url(self):
        messages.success(self.request, _('Usuario creado correctamente.'))
        return self.reverse('auth:user_list')


class MarketUpdateUser(MarketMixin, UpdateUser):
    def get_success_url(self):
        return self.reverse('auth:user_list')