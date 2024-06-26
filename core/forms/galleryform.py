from django import forms
from django.forms import formset_factory

from core.models import GalleryPhoto


class PhotoGalleryForm(forms.ModelForm):
    photo = forms.FileField(required=False)
    photo_id = forms.CharField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = GalleryPhoto
        fields = ['order', 'photo', 'title']
        widgets = {
            'photo': forms.FileInput(attrs={}),
        }

    @staticmethod
    def getGalleryFormset(gallery=None):

        extra_forms = 1 if (gallery is None or gallery.photos.count() == 0) else 0
        return formset_factory(PhotoGalleryForm, extra=extra_forms, can_delete=True)

    @staticmethod
    def get_initial(gallery=None):
        if gallery is None:
            return None

        photos_data = []
        for photo in gallery.photos.all():
            photos_data.append({
                'order': photo.order,
                'title': photo.title,
                'photo': photo.photo,
                'photo_id': photo.pk
            })

        return photos_data

    @staticmethod
    def save_galleryphoto(gallery, gallery_formset):

        if gallery is None:
            return

        # Remove previous gallery photos to save new ones
        GalleryPhoto.objects.filter(gallery=gallery).delete()
        for photo_form in gallery_formset:
            photo = photo_form.save(commit=False)
            if not photo.photo or photo_form.cleaned_data.get('DELETE'):
                continue
            photo.gallery = gallery
            photo.save()
