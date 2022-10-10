from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.


UserModel: AbstractUser = get_user_model()


class Organizations(models.Model):
    user = models.OneToOneField(UserModel,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="organization"
                             )
    name = models.CharField(max_length=128, blank=False, null=False)

    description = models.TextField(blank=True, null=True)
    # members =
    # OrgImg =
    # country =
    # city =
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("org", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Organizations, self).save(*args, **kwargs)



#**************************moved******************************
# class AdditionalServices(models.Model):
#     service = models.TextField()
#     price = models.PositiveIntegerField()