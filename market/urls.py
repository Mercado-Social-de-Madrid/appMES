from django.urls import path

from market import views

app_name = 'market'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),

    # Superadmin market management
    path('m/', views.MarketList.as_view(), name='market_list'),
    path('m/add', views.AddMarket.as_view(), name='add_market'),
    path('m/<pk>', views.EditMarket.as_view(), name='edit_market'),

    #### Market management #####
    path('<market>/dashboard/', views.MarketDashboard.as_view(), name='market_dashboard'),

    # Category
    path('<market>/categories/', views.CategoryList.as_view(), name='category_list'),
    path('<market>/categories/add', views.CategoryCreate.as_view(), name='add_category'),
    path('<market>/categories/<pk>', views.CategoryDetail.as_view(), name='category_detail'),

    # Providers
    path('<market>/providers/', views.ProviderList.as_view(), name='provider_list'),
    path('<market>/providers/add', views.CreateProvider.as_view(), name='add_provider'),
    path('<market>/providers/<pk>/edit', views.UpdateProvider.as_view(), name='edit_provider'),

    # Consumers
    path('<market>/consumers/', views.ConsumerList.as_view(), name='consumer_list'),
    path('<market>/consumers/add', views.CreateConsumer.as_view(), name='add_consumer'),
    path('<market>/consumers/<pk>', views.ConsumerDetail.as_view(), name='detail_consumer'),
    path('<market>/consumers/<pk>/edit', views.ConsumerEdit.as_view(), name='edit_consumer'),

    # Single registration account views
    path('dashboard/', views.UserDashboard.as_view(), name='user_dashboard'),
]

'''
    path('member/card/', views.member_card, name='member_card'),
    path('member/card_pdf/', views.member_card_pdf, name='member_card_pdf'),
    path('member/check/', views.CheckMemberStatus.as_view(), name='member_check_form'),
    path('socia/', views.MemberCheck.as_view(), name='member_check'),

    # Market admin urls

    path('entity/balance/<pk>/', views.HomeView.as_view(), name='entity_balance'),
    path('balance/<member_id>/', views.HomeView.as_view(), name='balance_detail'),

    

    path('<m>/categories/<pk>/edit/', views.HomeView.as_view(), name='category_edit'),

    path('<m>/dashboard/'),
    path('<m>/providers/'),
    path('<m>/providers/<pk>'),
    path('<m>/providers/<pk>/edit'),

    path('<m>/consumers/'),
    path('<m>/consumers/<pk>'),
    path('<m>/consumers/<pk>/edit'),
'''