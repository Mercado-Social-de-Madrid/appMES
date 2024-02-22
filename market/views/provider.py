from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from core.forms.galleryform import PhotoGalleryForm
from core.forms.social_profiles import SocialProfileForm, ProviderSocialProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.FormsetView import FormsetView
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.models import Gallery
from market.forms.provider import ProviderForm
from market.mixins.current_market import MarketMixin
from market.models import Category, Provider


class ProviderList(MarketMixin,  ListItemUrlMixin, AjaxTemplateResponseMixin, ListView):
    template_name = 'provider/list.html'
    model = Provider
    objects_url_name = 'provider_detail'
    ajax_template_name = 'provider/query.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(node=self.node)


class CreateProvider(MarketMixin, CreateView, FormsetView):
    template_name = 'provider/create.html'
    model = Provider
    form_class = ProviderForm

    def get_named_formsets(self):
        return {
            'gallery': PhotoGalleryForm.getGalleryFormset(),
            'social_profiles': ProviderSocialProfileForm.getSocialProfileFormset()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(node=self.node)
        return context

    def formset_gallery_get_initial(self):
        return PhotoGalleryForm.get_initial()

    def formset_gallery_valid(self, gallery, provider):
        for photo_form in gallery:
            photo = photo_form.save(commit=False)
            if not photo.photo or photo_form.cleaned_data.get('DELETE'):
                continue
            photo.gallery = gallery
            photo.save()

    def formset_social_profiles_get_initial(self):
        return SocialProfileForm.get_initial()

    def formset_social_profiles_valid(self, social_profiles, provider):
        for social_profile_form in social_profiles:
            url = social_profile_form.cleaned_data.get("url")
            if url:
                social_profile = social_profile_form.save(commit=False)
                if social_profile:
                    social_profile.provider = provider
                    social_profile.save()

    def get_initial(self):
        return {
            'node': self.node,
            'latitude': self.node.latitude,
            'longitude': self.node.longitude,
        }

    def get_success_url(self):
        messages.success(self.request, _('Proveedora añadida correctamente.'))
        return self.reverse('market:provider_list')


class DetailProvider(MarketMixin, DetailView):
    template_name = 'provider/detail.html'
    model = Provider

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class UpdateProvider(MarketMixin, UpdateView, FormsetView):
    template_name = 'provider/edit.html'
    model = Provider
    form_class = ProviderForm

    def get_named_formsets(self):
        return {
            'gallery': PhotoGalleryForm.getGalleryFormset(),
            'social_profiles': SocialProfileForm.getSocialProfileFormset()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(node=self.node)
        return context

    def formset_gallery_get_initial(self):
        return PhotoGalleryForm.get_initial(gallery=self.object.gallery)

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

        provider.gallery = gallery
        provider.save()

    def formset_social_profiles_get_initial(self):
        return SocialProfileForm.get_initial(initial_social_profiles=self.object.social_profiles)

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


    def get_success_url(self):
        messages.success(self.request, _('Proveedora actualizada correctamente.'))
        return self.reverse('market:provider_list')
