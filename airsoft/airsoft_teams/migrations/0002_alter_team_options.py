# Generated by Django 4.1.1 on 2023-02-12 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_teams", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"permissions": (("g_view_team", "View_team_guardian"),)},
        ),
    ]
