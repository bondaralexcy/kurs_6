# Generated by Django 4.2.13 on 2024-07-01 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0010_remove_message_mailing_remove_message_owner_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailing",
            name="clients",
        ),
        migrations.AddField(
            model_name="client",
            name="mailing",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailing",
                to="services.mailing",
                verbose_name="Рассылка",
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.EmailField(max_length=100, verbose_name="Электронная почта"),
        ),
    ]
