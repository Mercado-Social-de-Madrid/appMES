from modeltranslation.translator import register, TranslationOptions

from core.models import Node
from core.models.custom_text import CustomizableTextContext, NodeCustomText, CustomizableText


@register(Node)
class NodeTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(CustomizableTextContext)
class CustomizableTextContextTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(CustomizableText)
class CustomizableTextTranslationOptions(TranslationOptions):
    fields = ('help_text', 'description')

@register(NodeCustomText)
class NodeCustomTextTranslationOptions(TranslationOptions):
    fields = ('string', )