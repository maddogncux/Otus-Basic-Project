# Generated by Django 4.1.1 on 2022-12-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_event", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
