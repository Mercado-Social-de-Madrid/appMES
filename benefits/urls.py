from django.urls import path

from benefits import views

app_name = 'benefits'
urlpatterns = [

    path('<int:market>/benefits/', views.BenefitList.as_view(), name='list'),
    path('<int:market>/benefits/add/', views.BenefitCreate.as_view(), name='add'),
    path('<int:market>/benefits/<pk>/', views.BenefitDetail.as_view(), name='detail'),
    path('<int:market>/benefits/<pk>/edit/', views.BenefitUpdate.as_view(), name='edit'),
    path('<int:market>/benefits/<pk>/delete/', views.BenefitDelete.as_view(), name='delete'),
    path('<int:market>/providers/<pk>/add_benefit/', views.BenefitCreate.as_view(), name='add_provider_benefit'),

    path('benefit/', views.BenefitDetail.as_view(), name='user_benefit'),

]
