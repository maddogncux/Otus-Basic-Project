from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import CreateView, UpdateView

from airsoft_event.models import Event
# # from .forms import TeamRegForm
# from airsoft_teams.models import Team_Member
# from airsoft_teams.models import Team
from .forms import TeamRegForm
from .models import TeamRegistration, EventVote


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
        # member = get_object_or_404(Team_Member, user=self.request.user, main=True)
        obj.team = self.request.user.team_profile.team
        obj.event = get_object_or_404(Event, pk=self.kwargs["pk"])
        obj.save()
        return HttpResponseRedirect("/events/%s" % obj.event.id)


class TeamVoteRegistrationView(CreateView):
    model = TeamRegistration
    template_name = "registration.html"
    # form_class = TeamRegForm
    fields = ["side"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        team = self.request.user.team_profile.team
        obj.team = team
        obj.event = get_object_or_404(Event, pk=self.kwargs["pk"])
        vote = get_object_or_404(EventVote, event=obj.event, team=team)
        obj.save()
        obj.players.add(*vote.yes.all())
        form.save_m2m()
        vote.delete()
        return HttpResponseRedirect("/events/%s" % obj.event.id)


class VoteView(UpdateView):
    model = EventVote
    template_name = "vote.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            vote = get_object_or_404(EventVote, pk=self.kwargs["pk"])
            print("iam_here")
            vote.request_handler(request=request, user=self.request.user)
            return HttpResponseRedirect("/teams/%s" % vote.team.id)

