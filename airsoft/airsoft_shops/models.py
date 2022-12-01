from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()


class Shop(models.Model):
    owner = models.ForeignKey(UserModel, related_name="shop_owner", on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=True, null=False)
    description = models.TextField()
    logo = models.ImageField(upload_to="shop_logo", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    address = models.TextField()
    gps = models.CharField(max_length=124)
    membership = models.OneToOneField("airsoft_membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="shop_membership",
                                      primary_key=True
                                      )

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

