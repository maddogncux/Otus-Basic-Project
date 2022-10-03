from django.db import models
from typing import TYPE_CHECKING

# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length=64, blank=False, null=False)
    place = models.CharField(max_length=64, blank=False, null=False)                    # from poligon/place
    tags = models.ManyToManyField("event.EventTags", related_name="Tags")
    # organizer = models.ForeignKey                                      # must be created by founder
    # img = models.ImageField(upload_to='media')                       # Pillow required
    duration = models.DurationField('duration')                        # Date to Date
    body = models.TextField(blank=True, null=True)
    # rules =                                                  # make rules base on base rule + additional block by orgs
    additional_block1 = models.TextField(blank=True, null=True)
    # Date_creation =

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name


class EventPost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="post")
    name = models.CharField(max_length=64)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class EventTags(models.Model):
    name = models.TextField(max_length=16)

    def __str__(self):
        return self.name

















# class EventPlace(models.Model):
#     name = models.CharField(max_length=64, blank=False, null=False)
#     description = models.TextField(blank=True, null=True)
#     img =
#     navpoint =
#     owner =
#
#     def __str__(self):
#         return self.name
