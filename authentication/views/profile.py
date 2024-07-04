from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils import translation
from django.views.generic import FormView

from authentication.forms.password import PasswordForm
from authentication.forms.user import ProfileForm
from authentication.models.preregister import PreRegisteredUser
from market.mixins.current_market import MarketMixin
from django.views.i18n import set_language, LANGUAGE_QUERY_PARAMETER
from django.conf.urls import i18n
class EditProfile(MarketMixin, LoginRequiredMixin, FormView):
    template_name = 'user/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('auth:edit_profile')

    def user_can_access(self):
        return True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        user = form.save()
        translation.activate(user.preferred_locale)

        messages.success(self.request, 'Perfil actualizado correctamente')
        response = super().form_valid(form)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user.preferred_locale)
        return response

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


class PasswordResetView(PasswordResetConfirmView):
    success_url = reverse_lazy("auth:password_reset_complete")

    def form_valid(self, form):
        # if the user is preregistered, we consider the password reset as an activation
        PreRegisteredUser.objects.filter(user=self.user).delete()
        return super().form_valid(form)

def set_language_and_save_profile(request):
    response = set_language(request)
    if request.user.is_authenticated:
        user = request.user
        user.preferred_locale = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        user.save()
    return response
