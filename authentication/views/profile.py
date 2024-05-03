from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from authentication.forms.password import PasswordForm
from authentication.forms.user import ProfileForm
from market.mixins.current_market import MarketMixin


class EditProfile(MarketMixin, LoginRequiredMixin, FormView):
    template_name = 'user/profile.html'
    form_class = ProfileForm

    def user_can_access(self):
        return True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Perfil actualizado correctamente')
        return reverse_lazy('auth:edit_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = self.get_form()
        context['password_form'] = PasswordForm(user=self.request.user)
        context['profile_tab'] = True
        return context

class EditProfilePassword(MarketMixin, LoginRequiredMixin, FormView):
    template_name = 'user/profile.html'
    form_class = PasswordForm

    def user_can_access(self):
        return True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Contraseña actualizada correctamente')
        return reverse_lazy('auth:edit_profile')

    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Important!
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(instance=self.request.user)
        context['password_form'] = self.get_form()
        context['password_tab'] = True
        return context
