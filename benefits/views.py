from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView
from django_filters import FilterSet, BooleanFilter
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget

from benefits.forms.benefitform import BenefitForm
from benefits.models import Benefit
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.mixins.current_market import MarketMixin
from market.models import Provider

class BenefitsFilterForm(BootstrapForm):
    field_order = ['search', 'in_person', 'online', 'o', ]

class BenefitFilter(FilterSet):
    search = SearchFilter(names=['entity__name', 'benefit_for_entities', 'benefit_for_members'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['end_date', 'last_updated', 'published_date'],)
    in_person = BooleanFilter(field_name='in_person', widget=BooleanWidget(attrs={'class': 'threestate'}))
    online = BooleanFilter(field_name='online', widget=BooleanWidget(attrs={'class': 'threestate'}))

    class Meta:
        model = Benefit
        form = BenefitsFilterForm
        fields = {'in_person', 'online' }


class BenefitList(FilterMixin, MarketMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    model = Benefit
    objects_url_name = 'detail'
    template_name = 'benefits/list.html'
    ajax_template_name = 'benefits/query.html'
    filterset_class = BenefitFilter
    paginate_by = 7

    def get_queryset(self):
        return super().get_queryset().filter(entity__node=self.node)

    csv_filename = 'ventajas'
    available_fields = ['entity', 'active', 'published_date', 'benefit_for_entities', 'benefit_for_members',
                        'includes_intercoop_members', 'in_person', 'online', 'discount_code', 'discount_link_entities',
                        'discount_link_members']


class BenefitDetail(MarketMixin, DetailView):
    model = Benefit
    context_object_name = 'benefit'
    template_name = 'benefits/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_edit = self.request.user.is_superuser or self.request.user.is_staff
        context['can_edit'] = can_edit
        return context

    def get_object(self, queryset=None):
        if self.kwargs.get('pk'):
            return super().get_object(queryset)
        else:
            provider = Provider.objects.filter(owner=self.request.user).first()
            return Benefit.objects.filter(entity=provider).first()

    def user_can_access_resource(self, user):
        benefit = self.get_object()
        return not benefit or benefit.entity.owner == user


class BenefitCreate(MarketMixin, CreateView):
    model = Benefit
    form_class = BenefitForm
    template_name = 'benefits/add.html'

    def get_initial(self):
        return {
            'entity': self.kwargs.get('pk')
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider = self.kwargs.get('pk')
        if provider:
            context['provider'] = get_object_or_404(Provider, pk=provider)
        context['is_new'] = True
        context['ajax_url'] = self.reverse('market:provider_list') + '?filter=true'
        return context

    def get_success_url(self):
        return self.reverse('benefits:detail', kwargs={'pk': self.object.pk})


class BenefitUpdate(MarketMixin, UpdateView):
    model = Benefit
    form_class = BenefitForm
    template_name = 'benefits/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = self.object.entity
        return context

    def get_success_url(self):
        return self.reverse('benefits:detail', kwargs={'pk': self.object.pk})


class BenefitDelete(MarketMixin, DeleteView):
    model = Benefit
    template_name = 'benefits/delete.html'

    def get_success_url(self):
        return self.reverse('benefits:list')
