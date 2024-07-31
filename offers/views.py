# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView
from django_filters import FilterSet
from django_filters.views import FilterView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers import broadcast_notification, NotificationEvent
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.mixins.current_market import MarketMixin, AccountAccessMixin, OwnedByAccountAccessMixin
from market.models import Provider
from offers.forms.offer import OfferForm
from offers.models import Offer


class UserOffers(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        provider = Provider.objects.filter(owner=self.request.user).first()
        return reverse('offers:entity_offers', kwargs={ 'market': provider.node.pk, 'pk': provider.pk})

class ProviderOffers(AccountAccessMixin, MarketMixin, DetailView):
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


class CreateOffer(OwnedByAccountAccessMixin, MarketMixin, CreateView):
    template_name = 'offers/create.html'
    model = Offer
    form_class = OfferForm

    def get_initial(self):
        return {
            'provider': self.kwargs['pk']
        }

    def form_valid(self, form):
        offer = form.save()
        offer.save()

        broadcast_notification(
            node=offer.provider.node,
            event=NotificationEvent.OFFER_ADDED,
            title=lambda: offer.title,
            body=lambda: strip_tags(offer.description),
            data={'proveedora': offer.provider.name, 'id': str(offer.pk)},
            image=self.request.build_absolute_uri(offer.banner_thumbnail.url) if offer.banner_thumbnail.name else None,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Oferta añadida con éxito')
        return self.reverse('offers:entity_offers', kwargs={'pk': self.kwargs['pk'] })


class OffersFilterForm(BootstrapForm):
    field_order = ['search', 'o', ]


class OfferFilter(FilterSet):

    search = SearchFilter(names=['provider__name', 'title', 'description'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['end_date', 'begin_date', 'published_date'],)

    class Meta:
        model = Offer
        form = OffersFilterForm
        fields = { }


class OffersList(FilterMixin, MarketMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'offers/list.html'
    model = Offer
    filterset_class = OfferFilter
    objects_url_name = 'detail'
    ajax_template_name = 'offers/query.html'
    paginate_by = 8

    csv_filename = 'ofertas'
    available_fields = ['published_date', 'begin_date', 'end_date', 'title', 'description', 'provider__name']
    field_labels = {'published_date': _('Fecha de publicación')}

    def get_queryset(self):
        return super().get_queryset().filter(provider__node=self.node).order_by('-published_date').select_related('provider')


class OfferAccessMixin(object):
    def user_can_access_resource(self, user):
        offer = self.get_object()
        return user == offer.provider.owner

class OfferDetail(OfferAccessMixin, MarketMixin, DetailView):
    template_name = 'offers/detail.html'
    model = Offer


class OfferEdit(OfferAccessMixin, MarketMixin, UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offers/edit.html'

    def get_success_url(self):
        return self.reverse('offers:entity_offers', kwargs={'pk': self.object.provider.pk })


class OfferDelete(OfferAccessMixin, MarketMixin, DeleteView):
    template_name = 'offers/delete.html'
    model = Offer

    def get_success_url(self):
        messages.success(self.request, _('Oferta eliminada correctamente.'))
        return self.reverse('offers:entity_offers', kwargs={'pk': self.object.provider.pk })
