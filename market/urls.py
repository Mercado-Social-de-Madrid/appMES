from django.urls import path

from market import views

app_name = 'market'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),

    # Superadmin market management
    path('m/', views.MarketList.as_view(), name='market_list'),
    path('m/add/', views.AddMarket.as_view(), name='add_market'),
    path('m/<pk>/', views.EditMarket.as_view(), name='edit_market'),

    #### Market management #####
    path('<int:market>/dashboard/', views.MarketDashboard.as_view(), name='market_dashboard'),

    # Category
    path('<int:market>/categories/', views.CategoryList.as_view(), name='category_list'),
    path('<int:market>/categories/add/', views.CategoryCreate.as_view(), name='add_category'),
    path('<int:market>/categories/<pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<int:market>/categories/<pk>/delete', views.CategoryDelete.as_view(), name='delete_category'),

    # Providers
    path('<int:market>/providers/', views.ProviderList.as_view(), name='provider_list'),
    path('<int:market>/providers/add/', views.CreateProvider.as_view(), name='add_provider'),
    path('<int:market>/providers/<pk>/', views.DetailProvider.as_view(), name='provider_detail'),
    path('<int:market>/providers/<pk>/edit/', views.UpdateProvider.as_view(), name='edit_provider'),
    path('<int:market>/providers/<pk>/balance/', views.ProviderSocialBalance.as_view(), name='provider_balance'),
    path('<int:market>/providers/<pk>/delete/', views.DeleteProvider.as_view(), name='delete_provider'),

    # Consumers
    path('<int:market>/consumers/', views.ConsumerList.as_view(), name='consumer_list'),
    path('<int:market>/consumers/add/', views.CreateConsumer.as_view(), name='add_consumer'),
    path('<int:market>/consumers/<pk>/', views.ConsumerDetail.as_view(), name='detail_consumer'),
    path('<int:market>/consumers/<pk>/edit/', views.ConsumerEdit.as_view(), name='edit_consumer'),
    path('<int:market>/consumers/<pk>/delete/', views.DeleteConsumer.as_view(), name='delete_consumer'),

    # Single registration account views
    path('dashboard/', views.UserDashboard.as_view(), name='user_dashboard'),

    path('member/check/', views.CheckMemberStatus.as_view(), name='member_check_form'),
    path('member/card/', views.member_card, name='member_card'),
    path('member/card_pdf/', views.member_card_pdf, name='member_card_pdf'),
    path('socia/', views.MemberCheck.as_view(), name='member_check'),


    path('balance/<member_id>/', views.BalanceResult.as_view(), name='balance_result'),

    path('account/', views.UserAccountDetail.as_view(), name='user_account'),
    path('account/balance/', views.UserAccountSocialBalance.as_view(), name='account_balance'),
    path('<int:market>/account/<pk>/user/', views.ManageAccountUser.as_view(), name='account_user_detail'),
    path('<int:market>/info/', views.MarketInfoView.as_view(), name='market_info'),

]
