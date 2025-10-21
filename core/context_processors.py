import os

def export_vars(request):
    return {
        "VERSION_NUMBER": os.environ.get("APP_VERSION", "dev"),
        "ENV": os.environ.get("ENV")
    }