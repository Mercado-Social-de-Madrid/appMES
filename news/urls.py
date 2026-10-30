from django.urls import path
from news import views

app_name = 'news'
urlpatterns = [

    path('p/', views.ProviderNewsList.as_view(), name='provider_list'),
    path('p/add/', views.ProviderNewsCreate.as_view(), name='provider_add'),
    path('p/<pk>/', views.ProviderNewsDetail.as_view(), name='provider_detail'),
    path('p/<pk>/edit/', views.ProviderNewsUpdate.as_view(), name='provider_edit'),
    path('p/<pk>/delete/', views.ProviderNewsDelete.as_view(), name='provider_delete'),

    path('', views.NewsList.as_view(), name='list'),
    path('add/', views.NewsCreate.as_view(), name='add'),
    path('<pk>/', views.NewsDetail.as_view(), name='detail'),
    path('<pk>/edit/', views.NewsUpdate.as_view(), name='edit'),
    path('<pk>/delete/', views.NewsDelete.as_view(), name='delete'),

]