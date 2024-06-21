from django.core.management import BaseCommand
from services.mailing_task import send_email


class Command(BaseCommand):
    """Однократный запуск программы оправки сообщений"""

    def handle(self, *args, **options):
        send_email()
