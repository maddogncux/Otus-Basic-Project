from typing import TYPE_CHECKING
from django.db import models

# Create your models here.


class Team(models.Model):
    user_group = models.OneToOneField("airsoft_membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="team_owner",
                                      primary_key=True)
    description = models.TextField()                                      # move to basic_groupe
    chevron = models.ImageField(upload_to='chevron', blank=True)
    pattern = models.ManyToManyField("airsoft_gear.Pattern", blank=True)
    # accreditation = models.ManyToManyField()



    def __str__(self):
        return self.user_group.name

    if TYPE_CHECKING:
        objects: models.Manager

