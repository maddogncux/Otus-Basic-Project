# Generated by Django 4.1.1 on 2022-12-08 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_event", "0002_alter_event_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="scenario",
            name="body",
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]