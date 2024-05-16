from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_filters import FilterSet

from authentication.models.preregister import PreRegisteredUser
from core.forms.galleryform import PhotoGalleryForm
from core.forms.social_profiles import SocialProfileForm, ProviderSocialProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.FormsetView import FormsetView
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.models import Gallery, GalleryPhoto
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.filters.filtermixin import FilterMixin
from helpers.forms.BootstrapForm import BootstrapForm
from market.forms.provider import ProviderForm, CreateProviderForm
from market.mixins.current_market import MarketMixin, AccountAccessMixin
from market.models import Category, Provider
from django_filters.views import FilterView


class ProviderFilterForm(BootstrapForm):
    field_order = [ 'search', 'categories', 'o',]


class ProviderFilter(FilterSet):

    search = SearchFilter(names=['address', 'cif', 'name', 'email', 'member_id'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date', 'last_updated'],
                              field_labels={'last_name':'Apellido', 'registration_date':'Fecha de alta', 'last_updated':'ÚLtima actualización'})
    class Meta:
        model = Provider
        form = ProviderFilterForm
        fields = { 'categories' }


class ProviderList(FilterMixin, MarketMixin,  ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'provider/list.html'
    model = Provider
    filterset_class = ProviderFilter
    objects_url_name = 'provider_detail'
    ajax_template_name = 'provider/query.html'
    paginate_by = 15

    available_fields = ['cif', 'name', 'address', 'email', 'contact_phone', 'node',
                        'description', 'short_description', 'legal_form_title', 'num_workers', 'balance_detail' ]

    field_labels = {'node': _('Mercado'),}

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class ProviderFormSet(FormsetView):
    def get_named_formsets(self):
        return {
            'gallery': PhotoGalleryForm.getGalleryFormset(),
            'social_profiles': ProviderSocialProfileForm.getSocialProfileFormset()
        }

    def formset_gallery_get_initial(self):
        initial_data = None
        if self.object:
            initial_data = self.object.gallery
        return PhotoGalleryForm.get_initial(gallery=initial_data)

    def formset_gallery_valid(self, gallery_formset, provider):
        if provider.gallery is None:
            gallery = Gallery.objects.create()
        else:
            gallery = provider.gallery

        for photo_form in gallery_formset:
            photo = photo_form.save(commit=False)
            if not photo.photo or photo_form.cleaned_data.get('DELETE'):
                continue
            photo.gallery = gallery
            photo.save()

        for photo_form in gallery_formset.deleted_forms:
            photo_id = photo_form.cleaned_data.get('photo_id')
            if photo_id:
                GalleryPhoto.objects.filter(pk=photo_id).delete()
                # TODO: Delete also associated image file

        provider.gallery = gallery
        provider.save()

    def formset_social_profiles_get_initial(self):
        initial_data = None
        if self.object:
            initial_data = self.object.social_profiles
        return SocialProfileForm.get_initial(initial_social_profiles=initial_data)

    def formset_social_profiles_valid(self, social_profiles, provider):
        for social_profile_form in social_profiles:
            url = social_profile_form.cleaned_data.get("url")
            if url:
                try:
                    social_profile = provider.social_profiles.get(social_network=social_profile_form.cleaned_data.get("social_network"))
                except ObjectDoesNotExist:
                    social_profile = social_profile_form.save(commit=False)
                if social_profile:
                    social_profile.provider = provider
                    social_profile.url = url
                    social_profile.save()


class CreateProvider(MarketMixin, ProviderFormSet, CreateView):
    template_name = 'provider/create.html'
    model = Provider
    form_class = CreateProviderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(node=self.node)
        return context

    def get_initial(self):
        return {
            'node': self.node,
            'latitude': self.node.latitude,
            'longitude': self.node.longitude,
        }

    def form_valid(self, form):
        response = super().form_valid(form)
        preregister = form.cleaned_data['create_preregister']
        if preregister:
            PreRegisteredUser.create_user_and_preregister(self.object)
        return response

    def get_success_url(self):
        messages.success(self.request, _('Proveedora añadida correctamente.'))
        return self.reverse('market:provider_list')


class DetailProvider(AccountAccessMixin, MarketMixin, DetailView):
    template_name = 'provider/detail.html'
    model = Provider


class UpdateProvider(AccountAccessMixin, MarketMixin, ProviderFormSet, UpdateView):
    template_name = 'provider/edit.html'
    model = Provider
    form_class = ProviderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(node=self.node)
        return context

    def get_success_url(self):
        messages.success(self.request, _('Proveedora actualizada correctamente.'))
        return self.reverse('market:provider_detail', kwargs={'pk': self.object.pk})


class ProviderSocialBalance(DetailView):
    template_name = 'balance/detail.html'
    context_object_name = 'entity'
    model = Provider


class BalanceResult(DetailView):
    template_name = 'balance/results.html'
    context_object_name = 'entity'
    model = Provider

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Provider.objects.filter(member_id=self.kwargs['member_id']).first()


class DeleteProvider(MarketMixin, DeleteView):
    template_name = 'provider/delete.html'
    model = Provider

    # def delete(self, request, *args, **kwargs):
    #     Delete user owner?
    #     response = super().delete(request, *args, **kwargs)
    #     return response

    def get_success_url(self):
        messages.success(self.request, _('Proveedora eliminada correctamente.'))
        return self.reverse('market:provider_list')
