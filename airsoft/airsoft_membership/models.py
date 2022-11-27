from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()


class BasicGroup(models.Model):
    owner = models.ForeignKey(UserModel, related_name="owner", on_delete=models.PROTECT, blank=False)
    members = models.ManyToManyField(UserModel, related_name="member", blank=True)
    request_user = models.ManyToManyField(UserModel, related_name="request_user", blank=True)
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=False, null=False)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    # class Meta:
    #     abstract = True

    def add_member(self, new_member):
        if new_member not in self.members.all():
            if new_member != self.owner:
                self.members.add(new_member)
                self.request_user.remove(new_member)
                self.save()
                return BasicGroup

    def add_request(self, user_request):
        if user_request not in self.request_user.all():
            if user_request != self.owner:
                self.request_user.add(user_request)
                self.save()
                return BasicGroup

    def refuse_request(self, user_request):
        self.request_user.remove(user_request)
        self.save()
        return BasicGroup

    def kick_member(self, user_request):
        self.members.remove(user_request)
        self.save()
        return BasicGroup



class MembershipRequest(models.Model):
    group = models.ForeignKey(BasicGroup, related_name="membership_request", on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(UserModel, related_name="request_by", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
