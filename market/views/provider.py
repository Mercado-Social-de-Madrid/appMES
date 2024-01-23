from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView

from core.forms.galleryform import PhotoGalleryForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.FormsetView import FormsetView
from market.forms.provider import ProviderForm
from market.mixins.current_market import MarketMixin
from market.models import Category, Provider


class ProviderList(MarketMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'provider/list.html'
    model = Provider
    objects_url_name = 'provider_detail'
    ajax_template_name = 'provider/query.html'
    paginate_by = 15


class CreateProvider(MarketMixin, CreateView, FormsetView):
    template_name = 'provider/create.html'
    model = Provider
    form_class = ProviderForm

    def get_named_formsets(self):
        gallery_factory = PhotoGalleryForm.getGalleryFormset()
        initial_photos = PhotoGalleryForm.get_initial()
        return {
            'gallery': gallery_factory(initial=initial_photos)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(market=self.market)
        return context

    def formset_gallery_valid(self, gallery, provider):
        for photo_form in gallery:
            photo = photo_form.save(commit=False)
            if not photo.image or photo_form.cleaned_data.get('DELETE'):
                continue
            photo.gallery = gallery
            photo.save()

    def get_initial(self):
        return { 'market': self.market }

    def get_success_url(self):
        messages.success(self.request, _('Proveedora añadida correctamente.'))
        return self.reverse('market:provider_list')
