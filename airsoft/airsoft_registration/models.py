# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


UserModel: AbstractUser = get_user_model()


# move to event


class TeamRegistration(models.Model):
    event = models.ForeignKey("airsoft_event.Event",
                              on_delete=models.CASCADE,
                              related_name="registered_teams"
                              )
    side = models.ForeignKey("airsoft_event.Sides",
                             on_delete=models.PROTECT
                             )
    team = models.ForeignKey("airsoft_teams.Team",
                             related_name="team_registration",
                             on_delete=models.CASCADE
                             )
    players = models.ManyToManyField(UserModel,
                                     through="airsoft_registration.Player",
                                     related_name="regd_players"
                                     )
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    # services = models.ManyToManyField(services,related_name="add_team_services")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'team'], name='unique registration')
        ]

    def add_player(self, user):
        player = Player.get_or_create(team_reg=self.object, user=user)
        self.players.add(player)
        self.save()


    def loose_player(self, user):
        self.players.remove(user)
        self.save()


    def change_side(self, side):
        self.side = side
        self.save()

    def __str__(self):
        return self.team.name
    # def __str__(self):
    #     return self.event


class Player(models.Model):
    team = models.ForeignKey("airsoft_registration.TeamRegistration", on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, related_name="player", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    paid_time = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # services = models.ManyToManyField(services,related_name="add_player_services")


class EventVote(models.Model):
    event = models.ForeignKey("airsoft_event.Event", on_delete=models.CASCADE)
    team = models.ForeignKey("airsoft_teams.Team",
                             on_delete=models.CASCADE,
                             related_name="event_vote"
                             )
    yes = models.ManyToManyField(UserModel, related_name="Yes_player", blank=True)
    no = models.ManyToManyField(UserModel, related_name="No_player", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def request_handler(self, request, user):
        for key, value in request.POST.items():
            print(request.POST.items())
            print("check keys")
            print('Key: ', key)
            print('Value', value)
        if key == "yes":
            self.i_go(user)

        if key == "no":
            self.not_go(user)


    def i_go(self, user):
        self.yes.add(user)
        self.no.remove(user)
        self.save()


    def not_go(self, user):
        self.yes.remove(user)
        self.no.add(user)
        self.save()


    def self_delete(self):
        self.delete()
