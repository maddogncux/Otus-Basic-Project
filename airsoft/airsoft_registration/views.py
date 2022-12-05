from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import CreateView

from airsoft_event.models import Event
# from .forms import TeamRegForm
from airsoft_teams.models import Team
from .models import TeamRegistration


class TeamRegistrationView(CreateView):
    model = TeamRegistration
    template_name = "registration.html"
    # form_class = TeamRegForm
    fields = ["side", "players", ]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.team = get_object_or_404(Team, owner=self.request.user)
        obj.event = get_object_or_404(Event, pk=self.kwargs["pk"])
        obj.save()
        return super().form_valid(form)
