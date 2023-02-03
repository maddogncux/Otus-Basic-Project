from typing import TYPE_CHECKING
from airsoft_registration.models import EventVote
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
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

    def request_handler(self, request, user):
        for key, value in request.POST.items():
            print(request.POST.items())
            # print("check keys")
            # print('Key: %s' % (key))
            # print('Value %s' % (value))

        if key == "add_request":
            self.send_request(user=user)
            return self
        if key == "add":
            self.add_member(team_request=get_object_or_404(TeamRequest, pk=value))
            return self
        if key == "refuse":
            self.refuse_request(team_request=get_object_or_404(TeamRequest, pk=value))
            return self
        if key == "kick":
            self.kick_member(user=get_object_or_404(UserModel, pk=value))
            return self
        if key == "yes":
            vote = get_object_or_404(EventVote, pk=value)
            vote.i_go(user)
            return self
        if key == "no":
            vote = get_object_or_404(EventVote, pk=value)
            vote.not_go(user)
            return self
        # make role select in future
        if key == "promote":
            member = get_object_or_404(Members, pk=value)
            member.promote()
            return self
        if key == "depromote":
            member = get_object_or_404(Members, pk=value)
            member.depromote()
            return self
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
            team_request.self_delete
            return Team

    @staticmethod
    def refuse_request(team_request):
        team_request.self_delete()
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
    main = models.BooleanField(default=False) # chek if user in many teams
    # role = models.ForeignKey("airsoft_teams.Role", on_delete=models.SET_NULL, null=True)


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

    def promote(self):
        if self.role < 4:
            self.role=self.role + 1
            self.save()
            return self
    def depromote(self):
        if self.role > 1:
            self.role = self.role - 1
            self.save()
            return self
class TeamRequest(models.Model):
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # body = models.TextField()
    def __str__(self):
        return self.user.username

    def self_delete(self):
        self.delete()
