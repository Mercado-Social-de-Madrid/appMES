from django.conf import settings
from modeltranslation.utils import get_language
from django import template

from core.models.custom_text import CustomizableText, NodeCustomText

register = template.Library()

@register.simple_tag(takes_context=True)
def custom_text(context, node, text_id, *args, **kwargs):
    text = NodeCustomText.objects.filter(node=node, text_id=text_id ).first()
    return text.string if text else None

@register.simple_tag(takes_context=True)
def custom_text_description(context, text_id, *args, **kwargs):
    custom_text = CustomizableText.objects.filter(id=text_id).first()
    return custom_text.description if custom_text else None
