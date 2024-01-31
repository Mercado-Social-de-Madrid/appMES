# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

import helpers
from market.models import Provider
from offers.forms.offer import OfferForm

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.mixins.current_market import MarketMixin
from offers.models import Offer


@login_required
def user_offers(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_offers', entity_pk= entity.pk)
    elif type == 'person':
        messages.add_message(request, messages.ERROR, 'No tienes permisos para gestionar ofertas')
        return redirect('dashboard')
    else:
        return redirect('dashboard')

@login_required
def entity_offers(request, entity_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    is_owner = request.user == entity.user

    if not is_owner and not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver las ofertas de esta entitdad')
        return redirect('entity_detail', pk=entity.pk)

    current_offers = Offer.objects.current(entity=entity)
    future_offers = Offer.objects.future(entity=entity)
    past_offers = Offer.objects.past(entity=entity)

    return render(request, 'offers/entity_list.html', {
        'entity': entity,
        'current_offers': current_offers,
        'future_offers':future_offers,
        'past_offers':past_offers,
        'is_offers_owner': is_owner
    })


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


@login_required
def offer_edit(request, entity_pk, offer_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    offer = get_object_or_404(Offer, pk=offer_pk)
    can_edit = request.user.is_superuser or request.user == entity.user

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la oferta')
        return redirect('offer_detail', entity_pk=entity.pk, offer_pk=offer.pk )

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.entity = entity
            offer.save()

            return redirect('offer_detail', entity_pk=entity.pk, offer_pk=offer.pk)

    else:
        form = OfferForm(instance=offer)

    return render(request, 'offers/edit.html', {
        'offer': offer,
        'entity': entity,
        'form': form
    })