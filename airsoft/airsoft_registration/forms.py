from django.shortcuts import get_object_or_404

from airsoft_membership.models import BasicGroup
from airsoft_teams.models import Team
from .models import TeamRegistration
from django import forms

# class TeamRegForm(forms.Form):
#     class Meta:
#         model = TeamRegistration
#         fields = ["side", "players",]