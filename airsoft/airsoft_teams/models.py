from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.

UserModel: AbstractUser = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField()
    chevron = models.ImageField(upload_to='chevron/', blank=True, default='nopic.jpeg')
    pattern = models.ManyToManyField("airsoft_gear.Pattern", blank=True, default='nopic.jpeg')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="airsoft_teams.Members", related_name="memb")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    if TYPE_CHECKING:
        objects: models.Manager

    def get_absolute_url(self):
        return reverse("/teams/%s" % self.pk)

    def send_request(self, user):
        if user not in self.members.all():
            TeamRequest.objects.get_or_create(team=self, user=user)
            return Team

    def user_in_team(self, user):
        if user in self.members.all():
            return True
        else:
            return False

    def add_member(self, team_request):
        if team_request.user not in self.members.all():
            self.members.add(team_request.user)
            self.save()
            team_request.delete()
            return Team

    @staticmethod
    def refuse_request(team_request):
        team_request.delete()
        return Team

    def kick_member(self, user):
        self.members.remove(user)
        self.save()
        return Team





class Members(models.Model):
    FRIEND = 1
    MEMBER = 2
    MANAGER = 3
    OWNER = 4
    ROLE_CHOICES = (
        (FRIEND, 'friend'),
        (MEMBER, 'member'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),

    )
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=FRIEND)
    main = models.BooleanField(default=False)                                                                               # chek if user in many teams
    # role = models.ForeignKey("airsoft_teams.Role", on_delete=models.SET_NULL, null=True)
    # role

    def __str__(self):
        return self.user.username

    def set_owner(self):
        self.role = 4
        self.main = True
        self.save()
        return Members

    def set_role(self, role):
        self.role = role
        self.save()
        return Members


class TeamRequest(models.Model):
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # body = models.TextField()
    def __str__(self):
        return self.user.username

    # def refuse_request(self):
    #     self.delete()
    #     return Team