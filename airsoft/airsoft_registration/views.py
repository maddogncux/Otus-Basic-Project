from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import CreateView

from airsoft_event.models import Event
# from .forms import TeamRegForm
from airsoft_teams.models import Members
from airsoft_teams.models import Team
from .forms import TeamRegForm
from .models import TeamRegistration


class TeamRegistrationView(CreateView):
    model = TeamRegistration
    template_name = "registration.html"
    form_class = TeamRegForm
    # fields = ["side", "players", ]

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given team"""

        kwargs = super(TeamRegistrationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        member = get_object_or_404(Members, user=self.request.user, main=True)
        obj.team = member.team
        obj.event = get_object_or_404(Event, pk=self.kwargs["pk"])
        obj.save()
        return HttpResponseRedirect("/events/%s" % obj.event.id)
