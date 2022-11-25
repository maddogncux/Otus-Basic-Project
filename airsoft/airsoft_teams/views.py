from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from airsoft_membership.models import BasicGroup
from airsoft_teams.models import Team


class TeamListView(ListView):
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = (Team
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class TeamDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "team"
    model = BasicGroup
    template_name = "team_detail.html"
    queryset = (BasicGroup
                .objects
                # .select_related("user_group")
                .prefetch_related("membership_request")
                )


