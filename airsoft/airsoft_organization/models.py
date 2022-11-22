from django.db import models

# Create your models here.


class Organization(models.Model):
    user_group = models.OneToOneField("membership.BasicGroup",
                                      on_delete=models.CASCADE,
                                      related_name="org_owner",
                                      primary_key=True)
    Description = models.TextField()
    logo = models.FileField



    def __str__(self):
        return self.user_group.name