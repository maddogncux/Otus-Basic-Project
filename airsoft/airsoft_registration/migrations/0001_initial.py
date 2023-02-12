# Generated by Django 4.1.1 on 2023-02-12 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("airsoft_teams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("airsoft_event", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_paid", models.BooleanField(default=False)),
                ("paid_time", models.DateTimeField(blank=True, null=True)),
                ("approved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamRegistration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited", models.DateTimeField(auto_now=True)),
                ("approved", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="registered_teams",
                        to="airsoft_event.event",
                    ),
                ),
                (
                    "players",
                    models.ManyToManyField(
                        related_name="regd_players",
                        through="airsoft_registration.Player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "side",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="airsoft_event.sides",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_registration",
                        to="airsoft_teams.team",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="airsoft_registration.teamregistration",
            ),
        ),
        migrations.AddField(
            model_name="player",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="EventVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airsoft_event.event",
                    ),
                ),
                (
                    "no",
                    models.ManyToManyField(
                        blank=True,
                        related_name="No_player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_vote",
                        to="airsoft_teams.team",
                    ),
                ),
                (
                    "yes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="Yes_player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="teamregistration",
            constraint=models.UniqueConstraint(
                fields=("event", "team"), name="unique registration"
            ),
        ),
    ]
