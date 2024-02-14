from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from api.views import NodeViewSet, ProviderViewSet, CategoryViewSet
from api.views.auth import LoginView, LogoutView
from api.views.news import NewsViewSet

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet)
router.register("nodes", NodeViewSet)
router.register(r"providers/(?P<node>\w+)", ProviderViewSet)
router.register(r"categories/(?P<node>\w+)", CategoryViewSet)
router.register(r"news/(?P<node>\w+)", NewsViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/login/", LoginView.as_view()),
    path("v1/logout/", LogoutView.as_view()),
]


