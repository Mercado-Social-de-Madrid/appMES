from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from api.views import NodeViewSet, ProviderViewSet, CategoryViewSet
from api.views.auth import LoginView, LogoutView
from api.views.news import NewsViewSet

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet)
router.register("nodes", NodeViewSet)
router.register("providers", ProviderViewSet)
router.register("categories", CategoryViewSet)
router.register("news", NewsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]


