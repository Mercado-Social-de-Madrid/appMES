from modeltranslation.translator import register, TranslationOptions

from core.models import Node

@register(Node)
class NodeTranslationOptions(TranslationOptions):
    fields = ('name', 'multilang_enabled', )
