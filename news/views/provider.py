from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet

from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.forms.BootstrapForm import BootstrapForm
from market.mixins.provider import ProviderMixin
from news.models import News
from news.views import NewsCreate, NewsDetail, NewsUpdate, NewsDelete, NewsList


class NewsAccessMixin(object):
    def user_can_access_resource(self, user):
        news = self.get_object()
        return news.provider is not None and news.provider.owner == user


class NewsFilterForm(BootstrapForm):
    field_order = ['search', 'is_staff', 'is_superuser', 'o', ]

class NewsFilter(FilterSet):
    search = SearchFilter(names=['published_by__email', 'short_description', 'title'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['published_date', 'published_by'],)

    class Meta:
        model = News
        form = NewsFilterForm
        fields = { }

class ProviderNewsList(ProviderMixin, NewsList):
    template_name = 'news/provider/list.html'
    filterset_class = NewsFilter
    objects_url_name = 'provider_detail'
    ajax_template_name = 'news/provider/query.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node, provider=self.provider)


class ProviderNewsCreate(ProviderMixin, NewsCreate):
    template_name = 'news/provider/add.html'

    def form_valid(self, form):
        news = form.save()
        news.published_by = self.request.user
        news.provider = self.provider
        news.save()

        '''broadcast_notification(
            node=news.node,
            event=NotificationEvent.NEWS_ADDED,
            title=lambda: news.title,
            body=lambda: news.short_description,
            image=self.request.build_absolute_uri(news.banner_thumbnail.url) if news.banner_thumbnail.name else None,
            data={"id": str(news.pk)}
        )'''

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.reverse('news:provider_list')

    def user_can_access_resource(self, user):
        return True


class ProviderNewsDetail(NewsAccessMixin, NewsDetail):
    template_name = 'news/provider/detail.html'

class ProviderNewsUpdate(NewsAccessMixin, NewsUpdate):
    template_name = 'news/provider/edit.html'

    def get_success_url(self):
        messages.success(self.request, _('Noticia actualizada correctamente.'))
        return self.reverse('news:provider_list')


class ProviderNewsDelete(NewsAccessMixin, NewsDelete):
    template_name = 'news/provider/delete.html'
    model = News

    def get_success_url(self):
        messages.success(self.request, _('Noticia eliminada correctamente.'))
        return self.reverse('news:provider_list')
