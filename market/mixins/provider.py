from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import View

from market.models import Provider


class ProviderMixin(View):
    provider = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.provider = Provider.objects.filter(owner=self.request.user).first()