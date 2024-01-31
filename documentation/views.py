import logging
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

logger = logging.getLogger(__name__)


class DocsView(View):

    def get(self, request, *args, **kwargs):
        lang = kwargs['path']
        template_path = os.path.join(settings.BASE_DIR, 'documentation', 'site', lang, 'index.html')

        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin):
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()

                url = request.build_absolute_uri('/')
                logger.debug(url)
                content = content.replace('"assets/', f'"{url}static/')
                content = content.replace('"../assets/', f'"{url}static/')
                content = content.replace('"../../assets/', f'"{url}static/')
                content = content.replace('"img/', f'"{url}static/img/')
                content = content.replace('"../img/', f'"{url}static/img/')
                content = content.replace('"../../img/', f'"{url}static/img/')

                return HttpResponse(content)
        else:
            login_url = reverse('auth:login') + f'?next={request.path}'
            return HttpResponseRedirect(login_url)
