from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from market.forms.category import CategoryForm
from market.mixins.current_market import MarketMixin
from market.models import Category


# Create your views here.
class CategoryList(MarketMixin,  ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'category/list.html'
    model = Category
    objects_url_name = 'category_detail'
    ajax_template_name = 'category/query.html'
    paginate_by = 15

class CategoryCreate(MarketMixin, CreateView):
    template_name = 'category/create.html'
    form_class = CategoryForm
    model = Category

    def get_initial(self):
        return { 'market': self.market }

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