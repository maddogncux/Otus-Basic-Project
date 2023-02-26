from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
# Create your models here.
from django.urls import reverse

UserModel: AbstractUser = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=True, null=False)
    description = models.TextField()
    logo = models.ImageField(upload_to="org_logo", blank=True, default='nopic.jpeg')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through="airsoft_organization.Member",
                                     related_name="org_member")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"/organization/{self.pk}")

    def request_handler(self, request, user):
        for key, value in request.POST.items():
            print(request.POST.items())
            print('Key:', key)
            print('Value', value)
        if key == "add_request":
            self.send_request(user=user)

        if key == "add":
            self.add_member(org_request=get_object_or_404(OrgRequest, pk=value))

        if key == "refuse":
            self.refuse_request(org_request=get_object_or_404(OrgRequest, pk=value))

        if key == "kick":
            self.kick_member(user=get_object_or_404(UserModel, pk=value))

    def can_create_event(self, member):
        print("user role =", member.role)
        if member.role == 4:
            return True

    # def self_org(self, user):
    #     if user == self.owner:
    #         return self.objects

    def send_request(self, user):
        if user not in self.members.all():
            OrgRequest.objects.get_or_create(team=self, user=user)


    def user_in_org(self, user):
        if user in self.members.all():
            return True


    def add_member(self, org_request):
        if org_request.user not in self.members.all():
            self.members.add(org_request.user)
            self.save()
            org_request.self_delete()


    @staticmethod
    def refuse_request(org_request):
        org_request.self_delete()


    def kick_member(self, user):
        self.members.remove(user)
        self.save()



# edit roles for org
class Member(models.Model):
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
    org = models.ForeignKey("airsoft_organization.Organization",
                            on_delete=models.CASCADE,
                            related_name="org_members"
                            )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="org_profile"
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=FRIEND)

    def __str__(self):
        return self.user.username

    def set_owner(self):
        self.role = 4
        self.save()


    def set_role(self, role):
        self.role = role
        self.save()



class OrgRequest(models.Model):
    org = models.ForeignKey("airsoft_organization.Organization",
                            on_delete=models.CASCADE,
                            related_name="org_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def self_delete(self):
        self.delete()
