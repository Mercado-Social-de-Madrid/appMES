from django.urls import path, reverse_lazy

from authentication import views
from django.contrib.auth import views as auth_views

app_name = 'auth'
urlpatterns = [
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/password', views.profile_password, name='profile_password'),

    path('login/', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('auth:password_reset_done')), name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/add/', views.CreateUser.as_view(), name='add_user'),
    path('users/<pk>/', views.UpdateUser.as_view(), name='user_detail'),
    path('users/<pk>/delete', views.UserDelete.as_view(), name='user_delete'),

    path('<int:market>/users/', views.MarketUserList.as_view(), name='user_list'),
    path('<int:market>/users/add/', views.MarketCreateUser.as_view(), name='add_user'),
    path('<int:market>/users/<pk>/', views.MarketUpdateUser.as_view(), name='user_detail'),
    path('<int:market>/users/<pk>/delete', views.UserDelete.as_view(), name='user_delete'),

    path('register/<token>/', views.PreRegister.as_view(), name='preregister'),
    path('register/<token>/resend_email/', views.ResendPreregisterEmailAction.as_view(), name='preregister_send_email'),
]

'''
    path('registration/', views.UserListView.as_view(), name='users_list'),
    path('registration/<pk>/edit/', views.PasswordUpdateView.as_view(), name='edit_user'),

    '''