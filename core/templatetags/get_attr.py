import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)

@register.filter()
def get_form_field(obj, attr):
    return obj.__getitem__(attr)

@register.filter()
def get_attr(obj, attr):
    return getattr(obj, attr)
