# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from typing import TYPE_CHECKING
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from django.template.defaultfilters import slugify
# from django.urls import reverse
#
# # Create your models here.
#
# UserModel: AbstractUser = get_user_model()
#
#
# class Event(models.Model):
#
#     name = models.CharField(max_length=64, blank=False, null=False)
#     place = models.CharField(max_length=64, blank=False, null=False)
#     tags = models.ManyToManyField("event.EventTags", related_name="Tags", blank=True)
#     owner = models.ForeignKey("org.Organizations", on_delete=models.PROTECT, related_name="owner")  # must be created by founder
#     start_date = models.DateField()
#     end_date = models.DateField()
#     body = models.TextField(blank=True, null=True)
#     additional_block1 = models.TextField(blank=True, null=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
#     # img = models.ImageField(upload_to='media')                       # Pillow required
#     # rules =                                                  # make rules base on base rule + additional block by orgs
#     # Date_creation =
#     if TYPE_CHECKING:
#         objects: models.Manager
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("event", kwargs={"slug": self.slug})
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Event, self).save(*args, **kwargs)
#
#
# class EventPost(models.Model):
#     event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="post")
#     name = models.CharField(max_length=64)
#     body = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
#     # def save(self,):
#     #     post = form.save(commit=False)
#     #     post.event = get_object_or_404(Event, slug=self.kwargs['slug'])
#     #     post.save()
#     #     #     super(EventPost, self).save(*args, **kwargs)
#
#
#
# class EventTags(models.Model):
#     name = models.TextField(max_length=16)
#
#     def __str__(self):
#         return self.name
#
#
#
# class EventReg(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="event_reg")
#     teams = models.ManyToManyField("event.RegisteredTeams", blank=True, related_name="regd_teams")
#     # opened = models.BooleanField()
#     sides = models.ManyToManyField("event.Sides", related_name="sides", blank=True)
#     additionalservice = models.ManyToManyField("event.AdditionalServices", blank=True)
#
#     if TYPE_CHECKING:
#         objects: models.Manager
#
#
#
#     def __str__(self):
#         return self.event.name
#
#
# @receiver(signal=post_save, sender=Event)
# def reg_saved_handler(instance: Event, created: bool, **kwargs):
#     if not created:
#         return
#
#     EventReg.objects.create(event=instance)
#
#
# class AdditionalServices(models.Model):
#     service = models.TextField()
#     price = models.PositiveIntegerField()
#
# # must be related to org
# class Sides(models.Model):
#     event = models.ForeignKey(EventReg, on_delete=models.CASCADE, related_name="post")
#     side = models.CharField(max_length=64, blank=False, null=False)
#
#     def __str__(self):
#         return self.side
#
# # must a vote yes no mby with count inside team
# class RegisteredTeams(models.Model):
#     registration = models.ForeignKey(EventReg,related_name="registered", on_delete=models.CASCADE, blank=True, null=True)
#     team = models.ForeignKey("teams.Teams", on_delete=models.CASCADE, related_name="registered_team", blank=False)
#     yes = models.ManyToManyField(UserModel, related_name="yes", blank=True, null=True)
#     no = models.ManyToManyField(UserModel, related_name="no", blank=True, null=True)
#     mby = models.ManyToManyField(UserModel, related_name="mby", blank=True, null=True)
#     side = models.OneToOneField("event.Sides", on_delete=models.CASCADE)
#     addservice = models.ManyToManyField("event.AdditionalServices", blank=True)
#     registration_send = models.BooleanField(default=False, null=True)
#     # registration_confirmed = models.BooleanField()
#
#     def __str__(self):
#         return self.team.name
#
#
#
#
