from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

UserModel: AbstractUser = get_user_model()

class Advertisement(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="adv")
    name = models.CharField(max_length=128)
    description = models.TextField()

    if TYPE_CHECKING:
        objects: models.Manager


class Lot(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="lot")
    description = models.TextField()
    sold = models.BooleanField(default=False)


class LotPhoto(models.Model):
    Lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="callboard")
