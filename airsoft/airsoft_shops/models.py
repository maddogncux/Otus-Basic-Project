from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()


class Shop(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    city = models.CharField(max_length=64, blank=True, null=False)
    description = models.TextField()
    logo = models.ImageField(upload_to="shop_logo", blank=True, default='nopic.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    address = models.TextField()
    gps = models.CharField(max_length=124)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="airsoft_shops.Member", related_name="shop_member")

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name


class Member(models.Model):
    CONSULTANT = 1
    MEMBER = 2
    MANAGER = 3
    OWNER = 4
    ROLE_CHOICES = (
        (CONSULTANT, 'friend'),
        (MEMBER, 'member'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),

    )
    shop = models.ForeignKey("airsoft_shops.Shop", on_delete=models.CASCADE, related_name="shop_members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shop_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CONSULTANT)

    def __str__(self):
        return self.user.username

    def set_owner(self):
        self.role = 4
        self.save()
        return Member

    def set_role(self, role):
        self.role = role
        self.save()
        return Member

class ShopRequest(models.Model):
    team = models.ForeignKey("airsoft_shops.Shop", on_delete=models.CASCADE, related_name="shop_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username