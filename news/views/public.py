from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django_filters import FilterSet
from django_filters.views import FilterView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.fcm import broadcast_notification, NotificationEvent
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.mixins.current_market import MarketMixin
from news.forms.news import NewsForm
from news.models import News


class NewsFilterForm(BootstrapForm):
    field_order = ['search', 'is_staff', 'is_superuser', 'o', ]

class NewsFilter(FilterSet):
    search = SearchFilter(names=['published_by__email', 'short_description', 'title'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['published_date', 'published_by'],)

    class Meta:
        model = News
        form = NewsFilterForm
        fields = { }

class PublicNewsList(FilterMixin, MarketMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'news/list.html'
    model = News
    filterset_class = NewsFilter
    objects_url_name = 'detail'
    ajax_template_name = 'news/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)
