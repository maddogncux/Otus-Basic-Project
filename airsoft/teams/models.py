from typing import TYPE_CHECKING
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
UserModel: AbstractUser = get_user_model()


class Teams(models.Model):
    owner = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="team_owner")
    name = models.CharField(max_length=64, blank=False, null=False)
    city = models.CharField(max_length=64, blank=False, null=False)
    Description = models.TextField()
    # chevron = models.FileField
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # members = models.ManyToManyField(UserModel, through="Members", blank=True)
    members = models.ManyToManyField(UserModel, related_name="member", blank=True)
    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teams", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(self).save(*args, **kwargs)



# class TeamVote(models.Model)
#     question = models.ForeignKey()
#     answer













# class Members(models.Model):
#     team = models.ForeignKey(Teams, on_delete=models.CASCADE,
#     related_name="member_list", null=True, blank=True)
#     user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="member")
#     # all info airsoft info
#     # gear = models.ForeignKey(Gear)
#     #signal on user creat
#
#
#     def __str__(self):
#         return self.user.username
#
#     @receiver(signal=post_save, sender=UserModel)
#     def Member_handler(instance: UserModel, created: bool, **kwargs):
#         if not created:
#             return
#
#         Members.objects.create(user=instance)


class MemberRequests(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE,
                             related_name="request_list",
                             blank=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                             related_name="requests_by_user",
                             blank=False)
    request_text = models.TextField(blank=True)

    def __str__(self):
        return self.user























# if I found it does not mean that I stole





# class TeamRequest(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     accepted = models.CharField(blank=True, choices=TEAM_REQUEST_PERMIT_CHOICES, max_length=50)
#
#     def __str__(self):
#         return "%s - %s   " % (self.team.short_name, self.player.user.username)

# class Team(models.Model):
#     name = models.CharField(max_length=1024, null=False)
#     short_name = models.CharField(max_length=4, null=True)
#     players = models.ManyToManyField("Player", null=True)

#     logo = fields.ThumbnailerImageField(resize_source=dict(size=(200, 200), sharpen=True))
#     organisation = models.ForeignKey("Organisation", on_delete=models.CASCADE, null=True)
#     socialmedia = models.ManyToManyField("SocialMedia", null=True)
#     is_private = models.BooleanField(blank=True, default=False)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
