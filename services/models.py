from django.db import models
from django.utils import timezone

# from django.conf import settings

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """Класс для клиентов"""

    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.EmailField(
        max_length=100, verbose_name="Электронная почта", unique=True
    )

    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,verbose_name='владелец',**NULLABLE)

    def __str__(self):
        return f"ФИО: {self.name}, eMail: {self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("name",)


class Message(models.Model):
    """Класс для сообщения"""

    subject = models.CharField(max_length=50, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,verbose_name='владелец',**NULLABLE)

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
        max_length=20, choices=Periodicity, default=daily, verbose_name="периодичность"
    )
    start_time = models.DateTimeField(
        verbose_name="время начала отправки рассылки", **NULLABLE
    )
    end_time = models.DateTimeField(
        verbose_name="время окончания отправки рассылки", **NULLABLE
    )
    client = models.ManyToManyField(Client, verbose_name="Kлиенты для рассылки")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,verbose_name='владелец',**NULLABLE)

    def __str__(self):
        return f"Время: {self.start_time} - {self.end_time}, Статус: {self.status}, Периодичность: {self.periodicity}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

        # permissions = [
        #     ('change_status', 'Can change newsletters status'),
        # ]


class Logs(models.Model):
    """Класс для сбора статистики"""

    attempt_status = models.BooleanField(verbose_name="статус попытки")
    attempt_time = models.DateTimeField(verbose_name="дата и время последней попытки")
    response = models.CharField(
        max_length=100, verbose_name="ответ почтового сервера", **NULLABLE
    )

    mailing = models.ForeignKey(
        Mailing, verbose_name="рассылка", null=True, on_delete=models.SET_NULL
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
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
