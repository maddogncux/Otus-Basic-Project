from .models import Event
from django import forms


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "polygon", "Description", "banner", "arrival_date", "start_date", "end_date")
