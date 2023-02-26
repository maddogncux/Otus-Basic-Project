from django import forms
from .models import Event

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name",
                  "polygon",
                  "Description",
                  "banner",
                  "arrival_date",
                  "start_date",
                  "end_date")
