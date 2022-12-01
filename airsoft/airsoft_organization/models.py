from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse

UserModel: AbstractUser = get_user_model()


class Organization(models.Model):
    owner = models.ForeignKey(UserModel, related_name="org_owner", on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=True, null=False)
    description = models.TextField()
    logo = models.ImageField(upload_to="org_logo", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    membership = models.OneToOneField("airsoft_membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="org_membership",
                                      primary_key=True
                                      )


    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("/organization/%s" % self.pk)


    def can_create_event(self, user):
        if user == self.owner:
            return True
        else:
            return False


    def self_org(self, user):
        if user == self.owner:
            return self.objects
