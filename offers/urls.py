# -*- coding: utf-8 -*-

from django.urls import path
from offers import views

app_name = 'offers'
urlpatterns = [
    path('offers/', views.UserOffers.as_view(), name='user_list'),
    path('<int:market>/offers/', views.OffersList.as_view(), name='list'),
    path('<int:market>/providers/<pk>/offers/', views.ProviderOffers.as_view(), name='entity_offers'),
    path('<int:market>/providers/<pk>/add_offer/', views.CreateOffer.as_view(), name='add'),
    path('<int:market>/offers/<pk>/', views.OfferDetail.as_view(), name='detail'),
    path('<int:market>/offers/<pk>/edit/', views.OfferEdit.as_view(), name='edit'),
]
