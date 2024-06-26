from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.forms.category import CategoryForm
from market.mixins.current_market import MarketMixin
from market.models import Category


# Create your views here.
class CategoryList(MarketMixin, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'category/list.html'
    model = Category
    objects_url_name = 'category_detail'
    ajax_template_name = 'category/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class CategoryCreate(MarketMixin, CreateView):
    template_name = 'category/create.html'
    form_class = CategoryForm
    model = Category

    def get_initial(self):
        return { 'node': self.node }

    def form_valid(self, form):
        response = super(CategoryCreate, self).form_valid(form)
        messages.success(self.request, _('Categoría añadida correctamente.'))
        return response

    def get_success_url(self):
        return self.reverse('market:category_list', )


class CategoryDetail(MarketMixin, UpdateView):
    template_name = 'category/detail.html'
    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return self.reverse('market:category_detail', kwargs={'pk': self.object.pk})


class CategoryDelete(MarketMixin, DeleteView):
    template_name = 'category/delete.html'
    model = Category

    def get_success_url(self):
        messages.success(self.request, _('Categoría eliminada correctamente.'))
        return self.reverse('market:category_list')