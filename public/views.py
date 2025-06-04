from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django_filters import FilterSet
from django_filters.views import FilterView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from core.models import Node
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.mixins.current_market import MarketMixin
from market.models import Provider
from django.utils.translation import gettext_lazy as _

class IndexView(TemplateView):
    template_name = 'public/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markets'] = Node.objects.filter(visible=True)
        return context


class ProviderFilterForm(BootstrapForm):
    field_order = [ 'search', 'categories',]


class ProviderFilter(FilterSet):
    search = SearchFilter(names=['address', 'cif', 'name', 'email', 'member_id'], lookup_expr='in', label=_('Buscar...'))

    class Meta:
        model = Provider
        form = ProviderFilterForm
        fields = { 'categories' }


class CatalogView(XFrameOptionsExemptMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'public/provider/list.html'
    model = Provider
    filterset_class = ProviderFilter
    ajax_template_name = 'public/provider/query.html'
    paginate_by = 10
    model = Provider

    def get_queryset(self):
        node = self.get_node()
        return Provider.objects.filter(is_active=True, node=node)

    def get_node(self):
        return get_object_or_404(Node, shortname=self.kwargs.get('market_slug'))

    # Filter categories filterset by the categories of the current node
    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        cats_filter = filterset.filters['categories']
        cats_filter.queryset = cats_filter.queryset.filter(node=self.get_node())
        return filterset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.get_node()

        return context
