# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.mixins.current_market import MarketMixin
from market.models import Provider
from offers.forms.offer import OfferForm
from offers.models import Offer


class UserOffers(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        provider = Provider.objects.filter(owner=self.request.user).first()
        return reverse('offers:entity_offers', kwargs={ 'market': provider.node.pk, 'pk': provider.pk})

class ProviderOffers(MarketMixin, DetailView):
    model = Provider
    context_object_name = 'provider'
    template_name = 'offers/entity_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_offers': Offer.objects.current(provider=self.object),
            'future_offers': Offer.objects.future(provider=self.object),
            'past_offers': Offer.objects.past(provider=self.object),
        })
        return context

class CreateOffer(MarketMixin, CreateView):
    template_name = 'offers/create.html'
    model = Offer
    form_class = OfferForm

    def get_initial(self):
        return {
            'provider': self.kwargs['pk']
        }

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, 'Oferta añadida con éxito')
        return self.reverse('offers:entity_offers', kwargs={'pk': self.kwargs['pk'] })

class OffersList(MarketMixin, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'offers/list.html'
    model = Offer
    objects_url_name = 'detail'
    ajax_template_name = 'offers/query.html'
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(provider__node=self.node).order_by('-published_date').select_related('provider')


class OfferDetail(MarketMixin, DetailView):
    template_name = 'offers/detail.html'
    model = Offer


class OfferEdit(MarketMixin, UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offers/edit.html'

    def get_success_url(self):
        return self.reverse('offers:entity_offers', kwargs={'pk': self.object.provider.pk })
