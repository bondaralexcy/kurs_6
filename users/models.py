from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    """Добавил модель для пользователя.
    Задал электронную почту как поле для авторизации."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = PhoneNumberField(blank=True, null=True,)
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        null=True,
        blank=True,
        help_text="Загрузите свой аватар",
    )
    country = models.CharField(
        max_length=20,
        verbose_name="Страна",
        null=True,
        blank=True,
        help_text="Введите наименование страны пребывания",
    )
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('can_deactivate_user', 'Can deactivate User'),
        ]

    def __str__(self):
        return self.email
