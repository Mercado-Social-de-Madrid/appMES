from django.conf import settings


def version_number(request):
    return {"VERSION_NUMBER": settings.APP_VERSION}
