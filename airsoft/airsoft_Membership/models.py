from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()


class BasicGroup(models.Model):
    owner = models.ForeignKey(UserModel, related_name="owner", on_delete=models.PROTECT, blank=False)
    members = models.ManyToManyField(UserModel, related_name="member", blank=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    city = models.CharField(max_length=64, blank=False, null=False)
    is_private = models.BooleanField(default=False)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name


class MembershipRequest(models.Model):
    Group = models.ForeignKey(BasicGroup, related_name="Membership_request", on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(UserModel, related_name="request_by", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

