from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .django.yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(("collection_project.api.urls", "api"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += yasg_urlpatterns

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
