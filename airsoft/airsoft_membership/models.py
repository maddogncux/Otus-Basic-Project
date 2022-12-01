from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()





class BasicGroup(models.Model):
    members = models.ManyToManyField(UserModel, related_name="member", blank=True)
    request_user = models.ManyToManyField(UserModel, related_name="request_user", blank=True)
    is_private = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)


    if TYPE_CHECKING:
        objects: models.Manager

    # def __str__(self):
    #     return self.pk

    # class Meta:
    #     abstract = True

    def add_request(self, user):
        if user not in self.request_user.all():
            self.request_user.add(user)
            self.save()
            return BasicGroup

    def add_member(self, member):
        if member not in self.members.all():
            self.members.add(member)
            self.request_user.remove(member)
            self.save()
            return BasicGroup

    def refuse_request(self, member):
        self.request_user.remove(member)
        self.save()
        return BasicGroup

    def kick_member(self, member):
        self.members.remove(member)
        self.save()
        return self



