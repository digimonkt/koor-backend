"""KOOR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from decouple import config

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.contrib import admin
from django.urls import path, re_path
from django.template.loader import render_to_string

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from KOOR.settings import DJANGO_CONFIGURATION
# Swagger OpenAPI View
schema_view = get_schema_view(
   openapi.Info(
      title=config('DOCS_TITLE'),
      default_version=config('DEFAULT_VERSION'),
      description=render_to_string(config('DESCRIPTION')),
      terms_of_service=config('TERMS_OF_SERVICE'),
      contact=openapi.Contact(email=config('ORGANIZATION')),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/v1/user", include(('users.urls', 'users'), namespace='users_app_link')),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
