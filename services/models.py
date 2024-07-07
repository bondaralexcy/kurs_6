from django.db import models
from django.utils import timezone
from users.models import User

# from django.conf import settings

NULLABLE = {"null": True, "blank": True}


class Message(models.Model):
    """Класс для сообщения
    Сообщения не привязаны к рассылке  и являются общими для всех пользователей сервиса
    """

    subject = models.CharField(max_length=50, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """Класс для настройки рассылки"""

    ten_minutes = "каждые 10 минут"
    daily = "раз в день"
    weekly = "раз в неделю"
    monthly = "раз в месяц"

    Periodicity = [
        (ten_minutes, "Каждые 10 минут"),
        (daily, "Раз в день"),
        (weekly, "Раз в неделю"),
        (monthly, "Раз в месяц"),
    ]

    finished = "завершена"
    created = "создана"
    launched = "запущена"
    Status = [(finished, "завершена"), (created, "создана"), (launched, "запущена")]

    name = models.CharField(max_length=150, verbose_name="Название", **NULLABLE)
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=created,
        verbose_name="Статус рассылки",
    )
    periodicity = models.CharField(
        max_length=100, choices=Periodicity, default=daily, verbose_name="периодичность"
    )
    start_time = models.DateTimeField(
        verbose_name="время начала отправки рассылки", **NULLABLE
    )
    end_time = models.DateTimeField(
        verbose_name="время окончания отправки рассылки", **NULLABLE
    )
    # clients = models.ToManyField(Client, related_name='mailing', verbose_name="Клиенты для рассылки")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    is_active = models.BooleanField(verbose_name="Активная", default=True)
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        # Добавляем отдельные права для менеджера
        permissions = [
            ("can_deactivate_mailing", "Can deactivate mailing"),
            ("can_view_all_mailings", "Can view all mailings"),
        ]


class Client(models.Model):
    """Класс для клиентов
    Клиент принадлежит пользователю и может быть привязан к любой рассылке
    """

    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.EmailField(max_length=100, verbose_name="Электронная почта")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    mailing = models.ManyToManyField(
        Mailing, verbose_name="Рассылка", related_name="clients"
    )
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="clients",
    )

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("name",)


class Logs(models.Model):
    """Модель для сбора статистики

    Попытка рассылки:
    дата и время последней попытки;
    статус попытки (успешно / не успешно);
    ответ почтового сервера, если он был.
    """

    attempt_status = models.BooleanField(verbose_name="статус попытки")
    attempt_time = models.DateTimeField(verbose_name="дата и время последней попытки")
    response = models.CharField(
        max_length=150, verbose_name="ответ почтового сервера", **NULLABLE
    )
    mailing = models.ForeignKey(
        Mailing, verbose_name="рассылка", null=True, on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client, verbose_name="клиент", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.client} {self.mailing} {self.attempt_time} {self.attempt_status} {self.response}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылки"


class Contact(models.Model):
    """
    Контакты клиентов сервиса
    """

    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = models.TextField(verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="eMail")
    message = models.TextField(
        verbose_name="Сообщение", help_text="Введите сообщение контакта", **NULLABLE
    )
    time = models.DateTimeField(
        **NULLABLE,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
        default=timezone.now,
    )

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
