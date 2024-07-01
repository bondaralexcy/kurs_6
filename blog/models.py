from django.db import models
from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="заголовок")
    slug = models.CharField(max_length=100, verbose_name="slug", null=True, blank=True)
    content = models.TextField(verbose_name="содержимое")
    image = models.ImageField(
        verbose_name="изображение", blank=True, null=True, upload_to="blog/image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время создания"
    )
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")
    views_count = models.PositiveIntegerField(verbose_name="просмотры", default=0)
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        permissions = [
            ("can_reset_published", "Can Reset is_published"),
        ]
