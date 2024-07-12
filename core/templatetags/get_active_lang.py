from django.conf import settings
from modeltranslation.utils import get_language
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active_lang(context, lang, *args, **kwargs):
    market = context.get('current_market')
    active = get_language()

    if market and active not in market.enabled_langs:
        active = settings.MODELTRANSLATION_DEFAULT_LANGUAGE

    return lang == active
