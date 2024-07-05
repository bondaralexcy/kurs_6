from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Получение записей блога из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Blog.objects.all()
    else:
        key = 'blog_list'
        blogs = cache.get(key)
        if blogs is not None:
            return blogs
        else:
            blogs = Blog.objects.all()
            cache.set(key, blogs)
            return blogs


