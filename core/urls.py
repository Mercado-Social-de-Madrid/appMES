from django.urls import path

from core.views import CityView, AppLinksView

urlpatterns = [
    path(".well-known/assetlinks.json", AppLinksView.as_view()),
    path('ajax/load-cities/', CityView.as_view(), name='load_cities'),
]
