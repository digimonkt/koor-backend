import os
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
      title="Koor API",
      default_version='v1',
      description=render_to_string(os.path.join(DJANGO_CONFIGURATION.BASE_DIR,"..",'README.md')),
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@digimonk.in"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
