from django.urls import path
from news import views

app_name = 'news'
urlpatterns = [
    path('', views.NewsList.as_view(), name='list'),
    path('add/', views.NewsList.as_view(), name='add'),
    path('<pk>/', views.NewsList.as_view(), name='detail'),
    path('<pk>/edit', views.NewsList.as_view(), name='edit'),
    path('<pk>/delete', views.NewsList.as_view(), name='delete'),
]