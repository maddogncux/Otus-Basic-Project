# Generated by Django 4.1.1 on 2022-12-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_teams", "0004_alter_members_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="members",
            name="main",
            field=models.BooleanField(default=True),
        ),
    ]