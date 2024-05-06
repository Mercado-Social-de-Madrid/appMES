from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, FormView

from authentication.forms.user import UserForm, PasswordForm
from authentication.models import User
from authentication.models.preregister import PreRegisteredUser
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


class ChangeUserPassword(MarketMixin, FormView):
    template_name = 'user/password.html'
    form_class = PasswordForm
    user = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.user = User.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def form_valid(self, form):
        self.user = form.save(commit=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('auth:user_detail', kwargs={'pk': self.user.pk})


class CreateUser(CreateView):
    template_name = 'user/add.html'
    model = User
    form_class = UserForm

    def get_initial(self):
        initial = super().get_initial() or {}
        initial.update({'is_staff': True})
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        # Creating the preregistered user sends the welcome email
        PreRegisteredUser.objects.create(user=self.object)
        return response

    def get_success_url(self):
        messages.success(self.request, _('Usuario creado correctamente.'))
        return reverse('auth:user_list')


class UserDelete(MarketMixin, DeleteView):
    template_name = 'user/delete.html'
    model = User

    def get_success_url(self):
        messages.success(self.request, _('Usuario eliminado correctamente.'))
        return self.reverse('auth:user_list')

