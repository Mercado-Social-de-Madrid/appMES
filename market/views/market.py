import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ChoiceField
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView
from modeltranslation.fields import TranslationField

from authentication.mixins.admin import SuperuserAccessMixin
from core.forms.custom_text import NodeCustomTextForm
from core.forms.social_profiles import SocialProfileForm, NodeSocialProfileForm
from core.mixins.FormsetView import FormsetView
from core.models import Node
from core.models.custom_text import NodeCustomText, CustomizableTextContext
from market.forms.market import MarketForm, MarketPublicForm
from market.mixins.current_market import MarketMixin

logger = logging.getLogger(__name__)

class MarketList(SuperuserAccessMixin, ListView):
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


class AddMarket(SuperuserAccessMixin, CreateView, MarketFormsetView):
    template_name = 'market/create.html'
    form_class = MarketForm
    model = Node
    initial = {'preferred_locale': 'es' }

    def get_success_url(self):
        return reverse('market:market_list', )


@method_decorator(staff_member_required, name='dispatch')
class EditMarket(MarketMixin, UpdateView, MarketFormsetView):
    template_name = 'market/edit.html'
    pk_url_kwarg = 'market'
    form_class = MarketForm
    model = Node
    initial = {'preferred_locale': 'es'}

    def form_invalid(self, form):
        logger.debug(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return reverse('market:edit_market', kwargs={"market": self.object.pk})


@method_decorator(staff_member_required, name='dispatch')
class EditPublicMarket(MarketMixin, UpdateView, MarketFormsetView):
    template_name = 'market/public/edit.html'
    pk_url_kwarg = 'market'
    form_class = MarketPublicForm
    model = Node

    def get_named_formsets(self):
        formsets = super().get_named_formsets()
        formsets['node_custom_texts'] = NodeCustomTextForm.getNodeCustomTextsFormset()
        return formsets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text_contexts = CustomizableTextContext.objects.all()
        for text_ctx in text_contexts:
            text_ctx.formsets = []
            for form in context['formsets']['node_custom_texts']:
                for choice, text_id in form.fields['text_id'].choices:
                    if choice and choice.instance and choice.instance.context == text_ctx and form.initial['text_id'].id == choice.instance.id:
                        text_ctx.formsets.append({'form':form, 'instance': choice.instance } )

        context['text_contexts'] = text_contexts
        return context

    def formset_node_custom_texts_valid(self, custom_texts, node):
        for custom_text_form in custom_texts:
            try:
                custom_text = node.custom_texts.get(
                    text_id=custom_text_form.cleaned_data.get("text_id"))
            except ObjectDoesNotExist:
                custom_text = custom_text_form.save(commit=False)

            all_empty = True
            for f in custom_text_form.fields:
                if 'string' in f:
                    value = custom_text_form.cleaned_data.get(f)
                    setattr(custom_text, f, value)
                    if value or value != '':
                        all_empty = False

            if custom_text and not all_empty:
                custom_text.node = node
                custom_text.text_id = custom_text_form.cleaned_data.get("text_id")
                custom_text.save()
            elif custom_text and custom_text.pk:
                custom_text.delete()

    def formset_node_custom_texts_get_initial(self):
        initial_texts = NodeCustomText.objects.filter(node=self.node)
        return NodeCustomTextForm.get_initial(self.node, initial_texts)

    def form_invalid(self, form):
        logger.debug(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return reverse('market:edit_public_market', kwargs={"market": self.object.pk})


@method_decorator(staff_member_required, name='dispatch')
class MarketPreviewEmail(MarketMixin, DetailView):
    model = Node
    pk_url_kwarg = 'market'
    template_name = 'market/public/email_preview.html'

@method_decorator(staff_member_required, name='dispatch')
class MarketPreviewTemplate(MarketMixin, DetailView):
    model = Node
    pk_url_kwarg = 'market'
    template_name = 'market/public/template_preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(staff_member_required, name='dispatch')
class MarketPreviewEmailRender(MarketMixin, DetailView):
    model = Node
    pk_url_kwarg = 'market'
    template_name = 'market/public/email_render.html'

    def get_template_names(self):
        template_name = self.kwargs['template_name']
        return 'email/%s.html' % template_name

    def get_context_data(self, **kwargs):
        return {
            'token': 'token',
            'node': self.node,
            'user': self.request.user,
            'account': {'display_name':'{{tu_nombre}}'}
        }


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

