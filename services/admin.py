from django.contrib import admin
from services.models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "body",
    )
    search_fields = ("body",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "periodicity",
    )
    list_filter = (
        "status",
        "periodicity",
    )


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_status",
        "attempt_time",
        "response",
    )
    search_fields = (
        "client",
        "mailing",
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "message", "time")
