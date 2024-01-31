from django.urls import path

from benefits import views

app_name = 'benefits'
urlpatterns = [

    path('<market>/benefits/', views.BenefitList.as_view(), name='list'),
    path('<market>/benefits/add/', views.BenefitCreate.as_view(), name='add'),
    path('<market>/benefits/<pk>/', views.BenefitDetail.as_view(), name='detail'),
    path('<market>/benefits/<pk>/edit/', views.BenefitUpdate.as_view(), name='edit'),
    path('<market>/benefits/<pk>/delete/', views.BenefitDelete.as_view(), name='delete'),
    path('<market>/providers/<pk>/add_benefit/', views.BenefitCreate.as_view(), name='add_provider_benefit'),

    path('benefit/', views.BenefitDetail.as_view(), name='user_benefit'),

]
