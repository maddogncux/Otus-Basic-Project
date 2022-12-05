from django.contrib import admin

# Register your models here.
from .models import EventVote, TeamRegistration, Player
admin.site.register(TeamRegistration)
admin.site.register(Player)
