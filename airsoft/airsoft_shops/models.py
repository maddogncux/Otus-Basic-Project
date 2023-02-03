from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404

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
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="airsoft_shops.Member",
                                     related_name="shop_member")

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    def request_handler(self, request, user):
        for key, value in request.POST.items():
            print(request.POST.items())
            print("check keys")
            print('Key: %s' % (key))
            print('Value %s' % (value))
        if key == "add_request":
            self.send_request(user=user)
            return self
        if key == "add":
            self.add_member(team_request=get_object_or_404(ShopRequest, pk=value))
            return self
        if key == "refuse":
            self.refuse_request(team_request=get_object_or_404(ShopRequest, pk=value))
            return self
        if key == "kick":
            self.kick_member(user=get_object_or_404(UserModel, pk=value))
            return self
        if key == "promote":
            pass

    def send_request(self, user):
        if user not in self.members.all():
            ShopRequest.objects.get_or_create(shop=self, user=user)
            return self

    @staticmethod
    def refuse_request(shop_request):
        shop_request.self_delete()
        return

    def add_member(self, shop_request):
        if shop_request.user not in self.members.all():
            self.members.add(shop_request.user)
            self.save()
            shop_request.self_delete()
            return self

    def kick_member(self, user):
        self.members.remove(user)
        self.save()
        return self


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
    shop = models.ForeignKey("airsoft_shops.Shop", on_delete=models.CASCADE, related_name="shop_request")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def self_delete(self):
        self.delete()
