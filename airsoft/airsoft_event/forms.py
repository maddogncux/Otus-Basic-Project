from .models import Event
from django import forms


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__All__"
