from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.fcm import broadcast_notification, NotificationEvent
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
        return super().get_queryset().filter(node=self.node)


class NewsCreate(MarketMixin, CreateView):
    template_name = 'news/add.html'
    form_class = NewsForm
    model = News

    def get_initial(self):
        return { 'node': self.node }

    def form_valid(self, form):
        news = form.save()
        news.published_by = self.request.user
        news.save()

        broadcast_notification(
            node_shortname=news.node.shortname,
            event=NotificationEvent.NEWS_ADDED,
            title=news.title,
            body=news.short_description,
            image=self.request.build_absolute_uri(news.banner_thumbnail.url) if news.banner_thumbnail.name else None,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.reverse('news:list')


class NewsDetail(MarketMixin, UpdateView):
    template_name = 'news/edit.html'
    form_class = NewsForm
    model = News

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)

    def get_success_url(self):
        messages.success(self.request, _('Noticia actualizada correctamente.'))
        return self.reverse('news:list')


class NewsDelete(MarketMixin, DeleteView):
    template_name = 'news/delete.html'
    model = News

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)

    def get_success_url(self):
        messages.success(self.request, _('Noticia eliminada correctamente.'))
        return self.reverse('news:list')
