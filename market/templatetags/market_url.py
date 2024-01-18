from django.template import Library
from django.urls import reverse

register = Library()
UNSET = object()

@register.simple_tag(takes_context=True)
def market_url(context, view, market=UNSET, *args, **kwargs):

    if market is UNSET:
        print(context)
        market = context.get('current_market')

    if market:
        kwargs['market'] = market.pk

    return reverse(view, args=args, kwargs=kwargs)