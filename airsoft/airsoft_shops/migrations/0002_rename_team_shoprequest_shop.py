# Generated by Django 4.1.1 on 2023-02-03 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_shops", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shoprequest",
            old_name="team",
            new_name="shop",
        ),
    ]
