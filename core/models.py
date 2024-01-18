from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill

from helpers import RandomFileName


class Market(models.Model):

    name = models.CharField(max_length=150, verbose_name=_('Nombre'))
    shortname = models.CharField(max_length=10)
    visible = models.BooleanField(default=False, verbose_name=_('Visible en listado público'), help_text=_('Por defecto, un nuevo mercado empieza oculto hasta que esté listo para incluir en la aplicación'))
    latitude = models.FloatField(null=False, verbose_name=_('Latitud'), default=0)
    longitude = models.FloatField(null=False, verbose_name=_('Longitud'), default=0)

    class Meta:
        verbose_name = _('Mercado')
        verbose_name_plural = _('Mercados')


# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(Market, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Mercado que gestiona'))
    manages_multi = models.BooleanField(default=False, verbose_name=_('Maneja entidades en más de un mercado'))
    preferred_locale = models.CharField(default='es-ES', max_length=10, verbose_name=_('Idioma preferido de la interfaz'))

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

        permissions = (
            ("mespermission_can_manage_users", _("Puede ver la lista de usuarios")),
            ("mespermission_can_change_passwords", _("Puede cambiar la contraseña de un usuario")),
            ("mespermission_can_view_user_history", _("Puede consultar el historial de un usuario")),
            ("mespermission_can_update_users", _("Puede modificar usuarios")),
            ("mespermission_can_view_user_detail", _("Puede ver los detalles de un usuario")),
            ("mespermission_can_create_users", _("Puede añadir usuarios")),

        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def display_name(self):
        return self.get_full_name()


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