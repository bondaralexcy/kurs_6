import smtplib
from django.core.mail import send_mail
from django.conf import settings
from services.models import Client, Message, Mailing, Logs
from datetime import datetime, timedelta
import pytz

# def my_scheduled_job():
#     Client.objects.create(email='jack@mail.com',fio='jack logan',comment='bro')
# def sending_mail():
#     """ Прототип функции отправки сообщений
#         Проверка работоспособности почтового сервиса"""
#     print(settings.EMAIL_HOST_USER)
#     send_mail('Приветствие',
#               'Общее обращение',
#               settings.EMAIL_HOST_USER,
#               [settings.EMAIL_HOST_USER]
#               )


def send_email():
    """Отправка подготовленных рассылок"""
    for newsletter in Mailing.objects.all():
        # Цикл по всем рассылкам
        native_datetime = datetime.now()
        now = native_datetime.replace(tzinfo=pytz.utc)
        print("\n")
        print(newsletter.name)
        # print(newsletter.start_time)
        # print(now)
        # print(newsletter.end_time)
        if newsletter.start_time < now < newsletter.end_time:
            # Если настадо время, то меняем статус рассылки и отправляем сообщение
            newsletter.status = "запущена"
            print(f"Время пришло. Статус: {newsletter.status}")
            # Создаем список мейлов клиентов
            clients = newsletter.client.all()
            clients_email = []
            for client in clients:
                clients_email.append(getattr(client, "email"))

            # print(f"Список мейлов клиентов: {clients_email}")
            try:
                # Отправляем сообщение адресатам
                print(f"Отправляем сообщение: {newsletter.message.subject}")
                # print(newsletter.message.body)
                # print(settings.EMAIL_HOST_USER)
                # print(clients_email)
                send_mail(
                    subject=newsletter.message.subject,
                    message=newsletter.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=clients_email,
                    fail_silently=False,
                )
                attempt = True
                response = "Письмо успешно отправлено"
                print("Письмо успешно отправлено")

            except smtplib.SMTPException as exc:
                attempt = False
                response = f"Ошибка при отправке письма: {str(exc)}"
                print(f"Ошибка при отправке письма: {str(exc)}")

            finally:
                # Сохраняем лог
                for client in newsletter.client.all():
                    (
                        Logs.objects.create(
                            attempt_status=attempt,
                            attempt_time=now,
                            response=response,
                            mailing=newsletter,
                            client=client,
                        )
                    ).save()

            # Обновляем дату следующей отправки сообщения
            if newsletter.periodicity == "раз в день":
                newsletter.start_time += timedelta(days=1, hours=0, minutes=0)
            elif newsletter.periodicity == "раз в неделю":
                newsletter.start_time += timedelta(days=7, hours=0, minutes=0)
            elif newsletter.periodicity == "раз в месяц":
                newsletter.start_time += timedelta(days=30, hours=0, minutes=0)
            elif newsletter.periodicity == "каждые 10 минут":
                newsletter.start_time += timedelta(days=0, hours=0, minutes=10)

        elif now > newsletter.end_time:
            # Время рассылки закончено
            newsletter.status = "завершена"
            print(f"Время вышло. Статус: {newsletter.status}")
        elif now < newsletter.start_time:
            # Время рассылки пока не наступило
            newsletter.status = "создана"
            print(f"Еще не время. Статус: {newsletter.status}")
        newsletter.save()
