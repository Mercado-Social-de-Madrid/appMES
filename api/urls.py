from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from api.views import NodeViewSet, ProviderViewSet, CategoryViewSet
from api.views.auth import LoginView, LogoutView
from api.views.benefits import BenefitsViewSet
from api.views.news import NewsViewSet
from api.views.offers import OffersViewSet

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet)
router.register("nodes", NodeViewSet)
router.register(r"nodes/(?P<node>\d+)/providers", ProviderViewSet)
router.register(r"nodes/(?P<node>\d+)/categories", CategoryViewSet)
router.register(r"nodes/(?P<node>\d+)/news", NewsViewSet)
router.register(r"nodes/(?P<node>\d+)/offers", OffersViewSet)
router.register(r"nodes/(?P<node>\d+)/benefits", BenefitsViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/login/", LoginView.as_view()),
    path("v1/logout/", LogoutView.as_view()),
]


