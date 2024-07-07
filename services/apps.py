from time import sleep

from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services"

    def ready(self):
        return
        # для запуска django-apschedule при старте приложения
        # убрать return и раскомментировать следующие строки:

        # from services.management.commands.runapscheduler import Command
        # sleep(2)
        # Command.handle(self)
