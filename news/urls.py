from django.urls import path
from news import views

app_name = 'news'
urlpatterns = [
    path('', views.NewsList.as_view(), name='list'),
    path('add/', views.NewsCreate.as_view(), name='add'),
    path('<pk>/', views.NewsDetail.as_view(), name='detail'),
    path('<pk>/edit', views.NewsDetail.as_view(), name='edit'),
    path('<pk>/delete', views.NewsDelete.as_view(), name='delete'),
]