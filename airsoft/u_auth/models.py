from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django_countries import settings

UserModel: AbstractUser = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.user.username


@receiver(signal=post_save, sender=UserModel)
def user_saved_handler(instance: UserModel, created: bool, **kwargs):
    if not created:
        return

    UserProfile.objects.create(user=instance)
