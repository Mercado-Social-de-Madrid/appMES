import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)

@register.filter(name='get_attr')
def get_attr(obj, attr):
    return obj.__getitem__(attr)
