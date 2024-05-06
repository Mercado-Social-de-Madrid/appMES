
from django.urls import path

from reports import views

app_name = 'reports'
urlpatterns = [
    path('offers/', views.OffersChartView.as_view(), name='offers'),
    path('benefits/', views.BenefitsChartView.as_view(), name='benefits'),
]