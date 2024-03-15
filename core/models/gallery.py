from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill
from helpers import RandomFileName


class Gallery(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)

    class Meta:
        verbose_name = _('Galería')
        verbose_name_plural = _('Galerías')


class GalleryPhoto(models.Model):

    gallery = models.ForeignKey(Gallery, null=True, related_name='photos', on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name=_('Orden'), default=0)
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    photo = ProcessedImageField(upload_to=RandomFileName('photos/'), spec_id='gallery_photo',
                                processors=[ResizeToFit(1200, 1200, upscale=False)], format='JPEG')

    image_thumbnail = ImageSpecField(source='photo',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG', options={'quality': 70})

    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['order']