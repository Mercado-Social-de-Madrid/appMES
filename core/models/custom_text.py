from django.utils.translation import gettext_lazy as _
from django.db import models


# Models to define texts that are customizable per node
preview_types = (
    ('email', 'Previsualizar plantilla de email'),
    ('form', 'Campo o explicación dentro de un formulario')
)

class CustomizableTextContext(models.Model):
    id = models.CharField(primary_key=True, null=False, verbose_name=_('Identificador'), help_text=_('Identificador del texto'))
    title = models.TextField(blank=True, verbose_name=_('Título'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    preview_type = models.CharField(blank=True, null=True, choices=preview_types, verbose_name=_('Previsualización'))

    class Meta:
        verbose_name = 'Contexto de texto personalizable'
        verbose_name_plural = 'Contextos de texto personalizable'
        ordering = ['id']

    def __str__(self):
        return self.id


class CustomizableText(models.Model):
    id = models.CharField(primary_key=True, null=False, verbose_name=_('Identificador'), help_text=_('Identificador único del texto'))
    context = models.ForeignKey(CustomizableTextContext, null=True, verbose_name=_('Contexto en el que aparece'), on_delete=models.SET_NULL)
    description = models.TextField(blank=False, null=False, verbose_name=_('Etiqueta'), help_text=_('Cómo se muestra en los formularios'))
    help_text = models.TextField(blank=True, verbose_name=_('Descripción adicional'))

    class Meta:
        verbose_name = 'Texto personalizable'
        verbose_name_plural = 'Textos personalizables'
        ordering = ['id']

    def __str__(self):
        return self.id


class NodeCustomText(models.Model):
    node = models.ForeignKey("core.Node", verbose_name=_("Mercado"), on_delete=models.CASCADE, related_name="custom_texts")
    text_id = models.ForeignKey(CustomizableText, on_delete=models.CASCADE, related_name="node_values")
    string = models.TextField(blank=False, null=False, verbose_name=_('Texto'))

    class Meta:
        verbose_name = 'Texto personalizado'
        verbose_name_plural = 'Textos personalizados'
        ordering = ['text_id']

    def __str__(self):
        return '{}: {}'.format(self.node.name, self.text_id)