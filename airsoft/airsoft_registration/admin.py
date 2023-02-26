# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from django.contrib import admin

from airsoft_registration.models import TeamRegistration, Player, EventVote

# Register your models here.

admin.site.register(TeamRegistration)
admin.site.register(Player)
admin.site.register(EventVote)
