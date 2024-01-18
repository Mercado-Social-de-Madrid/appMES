from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView
from django.utils.translation import gettext as _
from market.forms.category import CategoryForm
from market.mixins.current_market import MarketMixin
from market.models import Category


# Create your views here.
class CategoryList(MarketMixin, ListView):
    template_name = 'category/list.html'
    model = Category


class CategoryCreate(MarketMixin, CreateView):

    form_class = CategoryForm
    model = Category
    template_name = 'category/create.html'

    def get_initial(self):
        return { 'market': self.market }

    def form_valid(self, form):
        response = super(CategoryCreate, self).form_valid(form)
        messages.success(self.request, _('Categoría añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('market:category_list', kwargs={'market':self.market.pk} )