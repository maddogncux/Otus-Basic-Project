from asyncio import Event

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
UserModel: AbstractUser = get_user_model()


class EventRegistration(models.Model):
    event = models.ForeignKey("airsoft_event.Event", related_name="registration", on_delete=models.CASCADE)
    registration_open = models.BooleanField(default=False)
    solo_allowed = models.BooleanField(default=False)


class Sides(models.Model):
    registration = models.ForeignKey(EventRegistration, related_name="event_registration", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)


class TeamRegistration(models.Model):
    sides = models.ForeignKey("airsoft_teams.Sides", related_name="team_on_side",)
    team = models.ForeignKey("airsoft_teams.Team", related_name="team_registration", on_delete=models.CASCADE)
    players = models.ManyToManyField("airsoft_registration.Player", related_name="regd_player")


class Player(models.Model):
    user = models.ManyToManyField(UserModel, related_name="player")
    is_paid = models.BooleanField(default=False)


class TeamBlock(models.Model):
    team = models.ManyToManyField(UserModel, related_name="event_to_go",)