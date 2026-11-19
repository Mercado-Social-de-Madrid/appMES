import os

from django.conf import settings


def export_vars(request):
    return {
        "VERSION_NUMBER": os.environ.get("APP_VERSION", "dev"),
        "ANALYTICS_SERVER_URL": settings.ANALYTICS_SERVER_URL,
        "ENV": os.environ.get("ENV")
    }