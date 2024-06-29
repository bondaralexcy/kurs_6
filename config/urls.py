# добавил ссылки на настройки работы с медиа-информацией + static
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("services.urls", namespace="services")),
    path("", include("blog.urls", namespace="blog")),
    path("users/", include("users.urls", namespace="users")),
]
# - настроить обработку вывода этих файлов для сервера разработки:
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
