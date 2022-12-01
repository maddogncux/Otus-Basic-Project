# Generated by Django 4.1.1 on 2022-11-29 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("airsoft_membership", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("airsoft_gear", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("name", models.CharField(max_length=64, unique=True)),
                ("city", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("chevron", models.ImageField(blank=True, upload_to="chevron")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited_at", models.DateTimeField(auto_now=True)),
                ("is_private", models.BooleanField(default=False)),
                (
                    "membership",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="team_membership",
                        serialize=False,
                        to="airsoft_membership.basicgroup",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="team_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pattern",
                    models.ManyToManyField(blank=True, to="airsoft_gear.pattern"),
                ),
            ],
        ),
    ]
