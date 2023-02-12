from typing import TYPE_CHECKING

from django.db import models

# Create your models here.
from django.urls import reverse


class Event(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)
    owner = models.ForeignKey("airsoft_organization.Organization",
                              on_delete=models.PROTECT,
                              related_name="event_owner"
                              )
    polygon = models.ForeignKey("airsoft_polygon.Polygon", on_delete=models.PROTECT, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    banner = models.ImageField(upload_to='event_banner', blank=True, default='nopic.jpeg')
    arrival_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    registration_open = models.BooleanField(default=False)
    solo_allowed = models.BooleanField(default=False)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("/event/%s" % self.pk)


class Sides(models.Model):

    name = models.CharField(max_length=128)
    hidden_scenario = models.BooleanField(default=False)
    scenario = models.ForeignKey("airsoft_event.Scenario", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Scenario(models.Model):
    body = models.TextField()