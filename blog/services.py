from django.core.cache import cache
from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Низкоуровневое кеширование
    Получение записей блога из кэша.
    Если кэш пуст,то получение из БД.
    """
    queryset = Blog.objects.all()
    if CACHE_ENABLED:
        key = "blog_list"
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)

        return cache_data

    return queryset
