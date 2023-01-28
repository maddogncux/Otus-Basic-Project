from django.db import models

# Create your models here.




class Polygon(models.Model):
    name = models.CharField(max_length=124)
    city = models.CharField(max_length=124,null=True)
    address = models.CharField(max_length=124)
    gps = models.CharField(max_length=124)
    # gps = DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    description = models.TextField(blank=True)


class PolygonPhoto(models.Model):
    polygon = models.ForeignKey(Polygon, related_name="photo", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="polygon")


class Maps(models.Model):
    polygon = models.ForeignKey(Polygon, related_name="maps", on_delete=models.CASCADE)
    maps = models.ImageField(upload_to="maps")
