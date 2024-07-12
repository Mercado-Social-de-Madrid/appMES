from django.conf import settings
from modeltranslation.utils import get_language
from django import template

register = template.Library()

@register.filter()
def get_active_lang(obj):
    current_language = get_language()
    if current_language in obj.enabled_langs:
        return current_language
    else:
        return settings.MODELTRANSLATION_DEFAULT_LANGUAGE