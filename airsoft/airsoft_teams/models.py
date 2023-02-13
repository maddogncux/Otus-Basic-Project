from typing import TYPE_CHECKING
from airsoft_registration.models import EventVote
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from guardian.shortcuts import assign_perm
# Create your models here.

UserModel: AbstractUser = get_user_model()

class Team_Member(models.Model):
    RECRUIT = 1
    MEMBER = 2
    MANAGER = 3
    OWNER = 4
    ROLE_CHOICES = (
        (RECRUIT, 'recruit'),
        (MEMBER, 'member'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),

    )
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_member")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=RECRUIT)

    def __str__(self):
        return self.user.username

    def request_handler(self, key, value):

        if key == "role":
            if 1 <= int(value) <= 4:   # set_owner up change for 3
                self.set_role(role=value)
                return self
        if key == "kick":
            self.kick()
            return self

    def set_owner(self):
        self.role = 4
        self.save()
        assign_perm('g_view_team', self.user, self.team)
        assign_perm('g_create_team_post', self.user, self.team)
        assign_perm('g_team_member_manager', self.user, self.team)
        assign_perm('g_team_vote', self.user, self.team)
        return self

    def set_role(self, role):
        self.role = role
        self.save()
        assign_perm('g_view_team', self.user, self.team)
        assign_perm('g_create_team_post', self.user, self.team)
        assign_perm('g_team_member_manager', self.user, self.team)
        assign_perm('g_team_vote', self.user, self.team)
        return self


    def kick(self):
        self.delete()



class Team(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField()
    chevron = models.ImageField(upload_to='chevron/', blank=True, default='nopic.jpeg')
    pattern = models.ManyToManyField("airsoft_gear.Pattern", blank=True, default='nopic.jpeg')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="member" , through="airsoft_teams.Team_Member")
    # frends = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="frends" , through="airsoft_teams.Team_Frends")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    # post = models.ForeignKey("airsoft_teams.Post", on_delete=models.PROTECT)
    # team_request = models.ForeignKey("airsoft_teams.TeamRequest", on_delete=models.PROTECT)



    class Meta:
        permissions = (
            ('g_view_team', 'View_team_guardian'),
            ('g_create_team_post', 'Creat_post_guardian'),
            ('g_team_member_manager', 'Mamber_manager_guardian'),
            ('g_team_vote','Team_vote_guardian')
        )

    # def request_handler(self, request, user):
    #     for key, value in request.items():
    #         print(request.POST.items())
    #         print("i am dumb")
    #         print(key)
    #         print(value)
    #
    #     if key == "add_request":\
    #         self.add_request(user)

    def __str__(self):
        return self.name

    if TYPE_CHECKING:
        objects: models.Manager

    def get_absolute_url(self):
        return reverse("/teams/%s" % self.pk)


    def add_request(self, user):
        if user not in self.members.all():
            TeamRequest.objects.get_or_create(team=self, user=user)
            return self


class TeamRequest(models.Model):
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # body = models.TextField()
    def __str__(self):
        return self.user.username

    def request_handler(self, key, value):
        if key =="add":
            self.add_member()
        if key == "refuse":
            self.refuse_request()
    def add_member(self):
        Team_Member.objects.create(user=self.user, team=self.team)
        self.delete()
        return self


    def refuse_request(self):
        self.self_delete()
        return Team


    def self_delete(self):
        self.delete()










#lets do this shit
# vk looks post sys
class TeamPost(models.Model):
    team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE,related_name="team_post",blank=False,null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="post_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    # imgs = (for add user pic)
    # avatar_of_user = (link to avatar \for opt and dont qs user each time )

class TeamPostComment(models.Model):
    post = models.ForeignKey("airsoft_teams.TeamPost", on_delete=models.CASCADE, related_name="team_comment")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="comment_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    # imgs = (for add user pic)
    # avatar_of_user = (link to avatar \for opt and dont qs user each time )


# class Members(models.Model):
#     FRIEND = 1
#     MEMBER = 2
#     MANAGER = 3
#     OWNER = 4
#     ROLE_CHOICES = (
#         (FRIEND, 'friend'),
#         (MEMBER, 'member'),
#         (MANAGER, 'manager'),
#         (OWNER, 'owner'),
#
#     )
#     team = models.ForeignKey("airsoft_teams.Team", on_delete=models.CASCADE, related_name="team_members")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_profile",)
#     created_at = models.DateTimeField(auto_now_add=True)
#     edited_at = models.DateTimeField(auto_now=True)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=FRIEND)
#     main = models.BooleanField(default=False) # chek if user in many teams
#     # role = models.ForeignKey("airsoft_teams.Role", on_delete=models.SET_NULL, null=True)


    # def __str__(self):
    #     return self.user.username
    #
    # def request_handler(self, key, value):
    #     if key == "role":
    #         self.set_role(role=value)
    #         return self
    #     # if key ==
    #
    # def set_owner(self, team):
    #     self.role = 4
    #     self.main = True
    #     self.save()
    #     # self.user.
    #     return self
    #
    # def set_role(self, role):
    #     self.role = role
    #     self.save()
    #     return Members
    #
    # def promote(self):
    #     if self.role < 4:
    #         self.role=self.role + 1
    #         self.save()
    #         return self
    # def depromote(self):
    #     if self.role > 1:
    #         self.role = self.role - 1
    #         self.save()
    #         return self