from django.urls import path
from django.views.generic import TemplateView

from public import views

app_name = 'public'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('creditos/', TemplateView.as_view(template_name='public/credits.html'), name='credits'),
    path('d/<market_slug>/', views.CatalogView.as_view(), name='provider_list'),
]
