from django.urls import path

from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),

    path('login/', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/r"reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
