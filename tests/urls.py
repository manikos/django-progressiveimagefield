from django.conf import settings
from django.urls import url, include
from django.conf.urls.static import static
# from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include('admin.site.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ] + urlpatterns
