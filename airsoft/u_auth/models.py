
"""doc string """
from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django_countries import settings

UserModel: AbstractUser = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="profile"
                                )
    avatar = models.ImageField(upload_to="avatars", default="no_avatar.png")
    city = models.CharField(max_length=32, null=True) # to citys
    country = models.CharField(max_length=32, null=True) # to country
    gear = models.CharField(max_length=32, null=True) # m2m to gear cat
    weapons = models.CharField(max_length=32, null=True) # m2m to  aeg's(gear)
    car = models.CharField(max_length=32, null=True) # m2m to car
    bbs = models.CharField(max_length=32, null=True) # m2m to bbs(gear)
    birthday = models.DateField(null=True)
    friend_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="friend")
    # team = models.OneToOneField("team)
    # subs = models.ManyToManyField()
    is_privet = models.BooleanField(default=False)
    team = models.ForeignKey("airsoft_teams.team",
                             on_delete=models.PROTECT,
                             related_name="user_profile",
                             null=True
                             )
    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.user.username


@receiver(signal=post_save, sender=UserModel)
def user_saved_handler(instance: UserModel, created: bool, **kwargs):
    if not created:
        return

    UserProfile.objects.create(user=instance)


class Car(models.Model):
    color = models.CharField(max_length=32, null=True)
    number = models.CharField(max_length=32, null=True)
    car_brand = models.CharField(max_length=32, null=True)
    model = models.CharField(max_length=32, null=True)
    combat_car = models.BooleanField(default=False)
