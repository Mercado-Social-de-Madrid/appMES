from django.urls import path

from core.views.app_links import AppLinksView

urlpatterns = [
    path(".well-known/assetlinks.json", AppLinksView.as_view())
]
