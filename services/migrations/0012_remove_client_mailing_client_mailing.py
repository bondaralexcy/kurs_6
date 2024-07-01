# Generated by Django 4.2.13 on 2024-07-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0011_remove_mailing_clients_client_mailing_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="mailing",
        ),
        migrations.AddField(
            model_name="client",
            name="mailing",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="mailing",
                to="services.mailing",
                verbose_name="Рассылка",
            ),
        ),
    ]
