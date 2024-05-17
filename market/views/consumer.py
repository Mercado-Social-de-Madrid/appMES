from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django_filters import FilterSet, BooleanFilter
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget

from authentication.models.preregister import PreRegisteredUser
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.forms.consumer import ConsumerForm, CreateConsumerForm
from market.mixins.current_market import MarketMixin
from market.models import Consumer


class ConsumerFilterForm(BootstrapForm):
    field_order = [ 'search', 'is_intercoop', 'o',]


class ConsumerFilter(FilterSet):

    search = SearchFilter(names=['address', 'cif', 'first_name', 'last_name', 'email', 'member_id'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date', 'last_updated'],
                              field_labels={'last_name':'Apellido', 'registration_date':'Fecha de alta', 'last_updated':'ÚLtima actualización'})
    is_intercoop = BooleanFilter(field_name='is_intercoop', widget=BooleanWidget(attrs={'class': 'threestate'}))


    class Meta:
        model = Consumer
        form = ConsumerFilterForm
        fields = {  }


class ConsumerList(FilterMixin, MarketMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'consumer/list.html'
    model = Consumer
    objects_url_name = 'detail_consumer'
    ajax_template_name = 'consumer/query.html'
    filterset_class = ConsumerFilter
    paginate_by = 15

    csv_filename = 'consumidoras'
    available_fields = ['cif', 'first_name', 'last_name', 'address', 'email', 'phone_numer', 'node',]

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class CreateConsumer(MarketMixin, CreateView):
    template_name = 'consumer/create.html'
    model = Consumer
    form_class = CreateConsumerForm

    def get_initial(self):
        return { 'node': self.node }

    def get_success_url(self):
        messages.success(self.request, _('Consumidora añadida correctamente.'))
        return self.reverse('market:consumer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        preregister = form.cleaned_data['create_preregister']
        if preregister:
            PreRegisteredUser.create_user_and_preregister(self.object)

        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

class ConsumerDetail(MarketMixin, DetailView):
    model = Consumer
    template_name = 'consumer/detail.html'


class ConsumerEdit(MarketMixin, UpdateView):
    model = Consumer
    form_class = ConsumerForm
    template_name = 'consumer/edit.html'

    def get_success_url(self):
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return self.reverse('market:detail_consumer', kwargs={'pk':self.object.pk})


class DeleteConsumer(MarketMixin, DeleteView):
    template_name = 'consumer/delete.html'
    model = Consumer

    # def delete(self, request, *args, **kwargs):
    #     Delete user owner?
    #     response = super().delete(request, *args, **kwargs)
    #     return response

    def get_success_url(self):
        messages.success(self.request, _('Consumidora eliminada correctamente.'))
        return self.reverse('market:consumer_list')