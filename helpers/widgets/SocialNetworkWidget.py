from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from core.models.social_profile import SocialNetwork


class SocialNetworkWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            social_network = SocialNetwork.objects.get(pk=value)
            args = {
                'field_name': name,
                'social_network': social_network
            }
            return mark_safe(render_to_string('widgets/social_network.html', args))
        return ''
