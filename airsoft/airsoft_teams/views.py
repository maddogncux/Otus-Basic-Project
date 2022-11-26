
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from airsoft_membership.models import BasicGroup, MembershipRequest
from airsoft_teams.models import Team

UserModel: AbstractUser = get_user_model()

class TeamListView(ListView):
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = (Team
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class TeamDetailView(DetailView):
    context_object_name = "team"
    model = BasicGroup
    template_name = "team_detail.html"
    queryset = (BasicGroup
                .objects
                # .select_related("user_group")
                .prefetch_related("membership_request")
                )

    def post(self, request, *args, **kwargs,):
        print(self.kwargs)
        print(self.args)
        if request.method == 'POST':
            for key, value in request.POST.items():
                print('Key: %s' % (key))
                # print(f'Key: {key}') in Python >= 3.7
                print('Value %s' % (value))
                # print(f'Value: {value}') in Python >= 3.7

            group = get_object_or_404(BasicGroup, pk=self.kwargs["pk"])
            if request.POST.get("add_requsete"):
                user_request = self.request.user
                BasicGroup.add_request(group, user_request)
                return HttpResponseRedirect("/teams/%s" % group.id)

            if request.POST.get("add"):
                new_member = get_object_or_404(UserModel, pk=value)
                print(new_member)
                BasicGroup.add_member(group, new_member)
                return HttpResponseRedirect("/teams/%s" % group.id)

            if request.POST.get("kick"):
                user_request = get_object_or_404(UserModel, pk=value)
                BasicGroup.kick_member(group, user_request)
                return HttpResponseRedirect("/teams/%s" % group.id)

            if request.POST.get("refuse"):
                user_request = get_object_or_404(UserModel, pk=value)
                BasicGroup.refuse_request(group, user_request)
                return HttpResponseRedirect("/teams/%s" % group.id)
        return HttpResponseRedirect("/teams/%s" % group.id)
