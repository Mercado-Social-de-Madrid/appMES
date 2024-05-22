from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from core.forms.social_profiles import SocialProfileForm, NodeSocialProfileForm
from core.mixins.FormsetView import FormsetView
from core.models import Node
from market.forms.market import MarketForm
from market.mixins.current_market import MarketMixin


class MarketList(ListView):
    template_name = 'market/list.html'
    model = Node


class MarketFormsetView(FormsetView):
    def get_named_formsets(self):
        return {
            'social_profiles': NodeSocialProfileForm.getSocialProfileFormset()
        }

    def formset_social_profiles_get_initial(self):
        initial_social_profiles = None
        if self.object:
            initial_social_profiles = self.object.social_profiles
        return SocialProfileForm.get_initial(initial_social_profiles=initial_social_profiles)

    def formset_social_profiles_valid(self, social_profiles, node):
        for social_profile_form in social_profiles:
            url = social_profile_form.cleaned_data.get("url")
            if url:
                try:
                    social_profile = node.social_profiles.get(
                        social_network=social_profile_form.cleaned_data.get("social_network"))
                except ObjectDoesNotExist:
                    social_profile = social_profile_form.save(commit=False)
                if social_profile:
                    social_profile.node = node
                    social_profile.url = url
                    social_profile.save()


class AddMarket(CreateView, MarketFormsetView):
    template_name = 'market/create.html'
    form_class = MarketForm
    model = Node

    def get_success_url(self):
        return reverse('market:market_list', )


class EditMarket(MarketMixin, UpdateView, MarketFormsetView):
    template_name = 'market/edit.html'
    pk_url_kwarg = 'market'
    form_class = MarketForm
    model = Node
    initial = {'preffered_locale': 'es-ES'}

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return reverse('market:edit_market', kwargs={"market": self.object.pk})


class MarketInfoView(MarketMixin, TemplateView):
    template_name = 'market/info/default.html'
    model = Node

    def get_template_names(self):
        return [f"market/info/{self.node.name.lower() }.html", "market/info/default.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.node.name
        return context

    def user_can_access(self):
        return True

