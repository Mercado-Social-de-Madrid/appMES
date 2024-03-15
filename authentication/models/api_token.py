
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy as DRFToken


class APIToken(DRFToken):
    class Meta:
        verbose_name = _('API Token')
        verbose_name_plural = _('API Tokens')
        proxy = True
