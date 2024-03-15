"""
URL configuration for appmes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from documentation.views import DocsView

urlpatterns = [
    path('admin/logs/', include('log_viewer.urls')),
    re_path(r"^docs/admin/(?P<path>.*)$", DocsView.as_view(), name="admin_docs"),
    re_path(r"^docs/user/(?P<path>.*)$", DocsView.as_view(), name="user_docs"),
    path('api/', include('api.urls')),
    path('', include('core.urls')),
    path('', include('market.urls')),
    path('', include('authentication.urls')),
    path('', include('benefits.urls')),
    path('', include('offers.urls')),
    path('<int:market>/news/', include('news.urls')),

    path('i18n/', include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
