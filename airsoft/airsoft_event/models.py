from typing import TYPE_CHECKING

from django.db import models

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    owner = models.ForeignKey("organization.Organization",
                              on_delete=models.PROTECT,
                              related_name="event_owner"
                              )
    polygon = models.ForeignKey("polygon.Polygon", on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    body = models.TextField(blank=True, null=True)
    Description = models.TextField()

    banner = models.ImageField(upload_to='event_banner', blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    if TYPE_CHECKING:
        objects: models.Manager
