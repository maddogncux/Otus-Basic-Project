from django.db import models

# Create your models here.




class Polygon(models.Model):
    name = models.CharField()
    address = models.CharField()
    gps = models.CharField()
    # gps = DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    description = models.TextField(blank=True)



class PolygonPhoto(models.Model):
    polygon = models.ForeignKey(Polygon, related_name="photo")
    photo = models.ImageField(upload_to="polygon")

class Maps(models.Model):
    polygon = models.ForeignKey(Polygon, related_name="maps")
    maps = models.ImageField(upload_to="maps")
