
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from authentication.models import User
from core.models import Node
from helpers import RandomFileName


class News(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name=_('Mercado en el que se publica'))
    published_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(null=True, blank=True, verbose_name=_('Título (máx 200 caracteres)'), max_length=250)

    short_description = models.TextField(null=True, blank=True, verbose_name=_('Descripción corta'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('news/'),
                                verbose_name=_('Imagen principal'),
                                processors=[ResizeToFit(756, 512, upscale=False)], format='JPEG')
    banner_thumbnail = ImageSpecField(source='banner_image',
                                       processors=[ResizeToFill(400, 200, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    published_date = models.DateTimeField(auto_now_add=True)
    more_info_text = models.CharField(null=True, blank=True, verbose_name=_('Texto del botón de info'), max_length=250)
    more_info_url = models.TextField(null=True, blank=True, verbose_name=_('URL con más información'))

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-published_date']

    def __unicode__(self):
        return self.title