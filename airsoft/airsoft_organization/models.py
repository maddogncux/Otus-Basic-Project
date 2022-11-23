from typing import TYPE_CHECKING

from django.db import models

# Create your models here.


class Organization(models.Model):
    user_group = models.OneToOneField("membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="org_owner",
                                      primary_key=True
                                      )
    Description = models.TextField()
    logo = models.ImageField(upload_to="org_logo", blank=True)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.user_group.name
