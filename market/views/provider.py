from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.forms.category import CategoryForm
from market.mixins.current_market import MarketMixin
from market.models import Category, Provider


class ProviderList(MarketMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'provider/list.html'
    model = Provider
    objects_url_name = 'provider_detail'
    ajax_template_name = 'provider/query.html'
    paginate_by = 15

