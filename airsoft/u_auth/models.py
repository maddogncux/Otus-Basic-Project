from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


UserModel: AbstractUser = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="profile")
    # team =  models.OneToOneField
    #  =

    if TYPE_CHECKING:
        objects: models.Manager


@receiver(signal=post_save, sender=UserModel)
def user_saved_handler(instance: UserModel, created: bool, **kwargs):
    if not created:
        return

    UserProfile.objects.create(user=instance)

