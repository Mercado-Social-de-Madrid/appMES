from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import RedirectURLMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import FormView

from authentication.forms.password import FirstPasswordForm
from authentication.models import User
from authentication.models.preregister import PreRegisteredUser


class PreRegister(FormView):

    template_name = 'registration/preregister.html'
    form_class = FirstPasswordForm

    def get_user_by_token(self):
        token = self.kwargs.get('token')
        return User.objects.filter(preregister__id=token, preregister__isnull=False).first()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_user_by_token()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user_by_token()
        if user:
            context['prereg_user'] = user
            context['account'] = user.accounts_managed.first()
        return context

    def form_valid(self, form):
        user = form.save()
        prereg_user = PreRegisteredUser.objects.get(id=self.kwargs.get('token'))
        if prereg_user:
            prereg_user.delete()

        messages.success(self.request, _('Contraseña actualizada correctamente'))
        return redirect('auth:edit_profile')

class ResendPreregisterEmailAction(RedirectURLMixin, View):
    def post(self, request, *args, **kwargs):
        prereg_user = PreRegisteredUser.objects.get(id=self.kwargs.get('token'))
        print(prereg_user)
        prereg_user.send_email()
        messages.success(self.request, _('Email de prerregistro reenviado'))

        return HttpResponseRedirect(self.get_success_url())
