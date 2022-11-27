from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from airsoft_event.models import Event


class EventCreateViews(CreateView):
    model = Event
    form_class = EventCreateForm