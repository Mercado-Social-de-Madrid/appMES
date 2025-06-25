from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.forms.intercoop import IntercoopForm
from market.mixins.current_market import MarketMixin
from market.models.intercoop import Intercoop


# Create your views here.
class IntercoopList(MarketMixin, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'intercoop/list.html'
    model = Intercoop
    objects_url_name = 'intercoop_detail'
    ajax_template_name = 'intercoop/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class IntercoopCreate(MarketMixin, CreateView):
    template_name = 'intercoop/create.html'
    form_class = IntercoopForm
    model = Intercoop

    def get_initial(self):
        return { 'node': self.node }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Intercooperación añadida correctamente.'))
        return response

    def get_success_url(self):
        return self.reverse('market:intercoop_list', )


class IntercoopDetail(MarketMixin, UpdateView):
    template_name = 'intercoop/detail.html'
    form_class = IntercoopForm
    model = Intercoop

    def get_success_url(self):
        return self.reverse('market:intercoop_detail', kwargs={'pk': self.object.pk})


class IntercoopDelete(MarketMixin, DeleteView):
    template_name = 'intercoop/delete.html'
    model = Intercoop

    def get_success_url(self):
        messages.success(self.request, _('Intercooperación eliminada correctamente.'))
        return self.reverse('market:intercoop_list')