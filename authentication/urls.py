from django.urls import path, reverse_lazy

from authentication import views
from django.contrib.auth import views as auth_views

from authentication.forms.password import PasswordReset

app_name = 'auth'
urlpatterns = [
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/edit/password', views.EditProfilePassword.as_view(), name='profile_password'),

    path('login/', views.LoginAndSetLang.as_view(), {'redirect_authenticated_user': True}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordReset, success_url=reverse_lazy('auth:password_reset_done')), name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', views.PasswordResetView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('users/', views.AdminUserList.as_view(), name='user_list'),
    path('users/add/', views.AdminCreateUser.as_view(), name='add_user'),
    path('users/<pk>/', views.AdminUpdateUser.as_view(), name='user_detail'),
    path('users/<pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('users/<pk>/password/', views.ChangeUserPassword.as_view(), name='user_password'),

    path('<int:market>/users/', views.MarketUserList.as_view(), name='user_list'),
    path('<int:market>/users/add/', views.MarketCreateUser.as_view(), name='add_user'),
    path('<int:market>/users/<pk>/', views.MarketUpdateUser.as_view(), name='user_detail'),
    path('<int:market>/users/<pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    path('<int:market>/users/<pk>/password', views.ChangeUserPassword.as_view(), name='user_password'),

    path('register/<token>/', views.PreRegister.as_view(), name='preregister'),
    path('register/<token>/resend_email/', views.ResendPreregisterEmailAction.as_view(), name='preregister_send_email'),
]
