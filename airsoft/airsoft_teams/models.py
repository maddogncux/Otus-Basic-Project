from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse

UserModel: AbstractUser = get_user_model()

class Team(models.Model):
    owner = models.ForeignKey(UserModel, related_name="team_owner", on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField()
    chevron = models.ImageField(upload_to='chevron', blank=True)
    pattern = models.ManyToManyField("airsoft_gear.Pattern", blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    membership = models.OneToOneField("airsoft_membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="team_membership",
                                      primary_key=True)
    def __str__(self):
        return self.name

    if TYPE_CHECKING:
        objects: models.Manager

    def get_absolute_url(self):
        return reverse("/teams/%s" % self.pk)
