# Generated by Django 4.2.13 on 2024-07-02 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("services", "0014_alter_client_mailing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="mailing",
            field=models.ManyToManyField(
                related_name="clients", to="services.mailing", verbose_name="Рассылка"
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
    ]
