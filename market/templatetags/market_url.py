from django.template import Library
from django.urls import reverse

register = Library()
UNSET = object()

@register.simple_tag(takes_context=True)
def market_url(context, view, *args, **kwargs):
    market = context.get('current_market')
    if market:
        if len(args) > 0:
            args = [market.pk] + list(args)
        else:
            kwargs['market'] = market.pk

    return reverse(view, args=args, kwargs=kwargs)