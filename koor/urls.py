from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

DEFAULT_VERSION = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('koor.v1_urls')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url='api/{0}/'.format(DEFAULT_VERSION), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
