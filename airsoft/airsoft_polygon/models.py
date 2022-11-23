from django.db import models

# Create your models here.

class polygon(models.Model):
    name = models.CharField()
    address = models.CharField()
    gps = models.CharField()
    photo = models.ManyToManyField()
    map = models.ImageField


