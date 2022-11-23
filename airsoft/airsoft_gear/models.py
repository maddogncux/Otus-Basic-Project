from django.db import models

# Create your models here.


class Pattern(models.Model):
    name = models.CharField()
    img = models.ImageField(upload_to="pattern", blank=True)
