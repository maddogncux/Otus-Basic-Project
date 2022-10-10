from django.db import models

# Create your models here.

class Org(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="profile")


class Organization(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    founder = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="Organization")
    description = models.TextField(blank=True, null=True)

    # OrgImg =
    # country =
    # city =

