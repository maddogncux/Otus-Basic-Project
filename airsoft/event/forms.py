from urllib import request

from django import forms
from .models import Event, EventPost, EventReg, AdditionalServices, RegisteredTeams


class EventForms(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "place", "body", "additional_block1", "end_date", "start_date", ]


class EventPostForms(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = ["name", "body"]


class EventRegForm(forms.ModelForm):
    class Meta:
        model = EventReg
        fields = ["event", "teams", "sides", "additionalservice"]


class EventAdditionalServicesForm(forms.ModelForm):
    class Meta:
        model = AdditionalServices
        fields = ["service", "price"]

# class RegisteredTeams(forms.ModelForm):
#
#     class Meta:
#         model = RegisteredTeams
#         fields = ["registration", "players", "side", "addservice"]
#         players = forms.ModelChoiceField("members")
