from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.shortcuts import get_object_or_404
from django.urls import reverse

UserModel: AbstractUser = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField()
    chevron = models.ImageField(upload_to='chevron', blank=True)
    pattern = models.ManyToManyField("airsoft_gear.Pattern", blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="airsoft_teams.Members")
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
            TeamRequest.objects.get_or_create(team=self.object, user=user)
            return Team

    def add_member(self, user):
        if user not in self.members.all():
            self.members.add(user)
            self.save()
            return Team

    def refuse_request(self, request):
        request.delete()
        return Team

    def kick_member(self, user):
        self.members.remove(user)
        self.save()
        return Team

    # def set_owner(self, user):
    #     obj = Members.objects.get(user=user, team=self)
    #     obj.role = ROLE_OWNER
    #     obj.save
    #     return Team

class Role(models.Model):

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

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=FRIEND)
    # role = models.ForeignKey("airsoft_teams.Role", on_delete=models.SET_NULL, null=True)
    # role

    def __str__(self):
        return self.team.name

    def set_owner(self):
        # self.role = get_object_or_404(Role, pk=4)
        self.role = 4
        self.save()
        return Members



class TeamRequest(models.Model):
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
