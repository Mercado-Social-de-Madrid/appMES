from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.mixins.current_market import MarketMixin
from news.forms.news import NewsForm
from news.models import News


# Create your views here.
class NewsList(MarketMixin,  ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'news/list.html'
    model = News
    objects_url_name = 'detail'
    ajax_template_name = 'news/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(market=self.market)


class NewsDetail(MarketMixin, UpdateView):
    template_name = 'news/detail.html'
    form_class = NewsForm
    model = News

    def get_queryset(self):
        return super().get_queryset().filter(market=self.market)