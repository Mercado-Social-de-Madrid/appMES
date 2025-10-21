import logging
import os
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from pathlib import Path

logger = logging.getLogger(__name__)


class DocsView(View):

    ALLOWED_LANGS = ["es", "eu", "ca", "gl"]

    def get(self, request, *args, **kwargs):
        docs_type = request.path.split('/')[2]
        path = kwargs["path"]

        template_path = os.path.join(settings.BASE_DIR, 'documentation', docs_type, 'site', path)

        if Path(template_path).is_dir():
            template_path = os.path.join(template_path, "index.html")

        if self.can_access_docs(request.user, docs_type):
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()

                url = request.build_absolute_uri('/')
                logger.debug(url)
                content = re.sub(r'"(../)*assets/', f'"{url}static/', content)
                content = re.sub(r'"(../)*img/', f'"{url}static/img', content)

                return HttpResponse(content)
        else:
            login_url = reverse('auth:login') + f'?next={request.path}'
            return HttpResponseRedirect(login_url)


    def can_access_docs(self, user, docs_type):
        return True # Docs public for everyone
