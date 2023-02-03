
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, DetailView, CreateView


from airsoft_registration.models import EventVote
from airsoft_teams.models import Team, Members, TeamRequest

UserModel: AbstractUser = get_user_model()


class TeamCreate(CreateView):
    template_name = "team_create.html"
    # success_url =
    model = Team
    # form_class =
    fields = ["name", "city", "description", "chevron", "pattern", "is_private"]

    def form_valid(self, form):
        user = self.request.user
        # user_in_team = Team.objects.filter(members=user)
        # if len(user_in_team) == 1:
        #     return HttpResponseRedirect("/teams/create/")
        # else:
        #     # go = None  # optio
        obj = form.save(commit=False)
        obj.save()
        obj.members.add(user)
        form.save_m2m()
        change_role = get_object_or_404(Members, user=user, team=obj)
        Members.set_owner(change_role)
        return HttpResponseRedirect("/teams/%s" % obj.id)


class TeamListView(ListView):
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = (Team
                .objects
                # .select_related()
                # .prefetch_related()
                .all())

class TeamMemberDetails(DetailView):
# class TeamDetails(DetailView):
    template_name = 'team_details.html'
    model = Team

class TeamDetails(DetailView):
# class TeamMemberDetails(DetailView):
    template_name = 'team_member_details.html'
    queryset = Team\
        .objects\
        .prefetch_related("team_request",
                          "event_vote",
                          "team_members",
                          "team_registration")\
        .select_related()


    def get_form_kwargs(self):
        kwargs = super(self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            team = get_object_or_404(Team, pk=self.kwargs["pk"])
            team.request_handler(request=request, user=self.request.user)
            return HttpResponseRedirect("/teams/%s" % team.id)
        return HttpResponseRedirect("/teams/%s" % team.id)





    # def post(self, request, *args, **kwargs, ):
    #     if request.method == 'POST':
    #         print("get post")
    #         for key, value in request.POST.items():
    #             print("check keys")
    #             print('Key: %s' % (key))
    #             print('Value %s' % (value))
    #         team = get_object_or_404(Team, pk=self.kwargs["pk"])
    #         print("get group")
    #         if request.POST.get("add_request"):
    #             print("add_request")
    #             Team.send_request(team, user=self.request.user)
    #             return HttpResponseRedirect("/teams/%s" % team.id)
    #         else:
    #             if request.POST.get("add"):
    #                 team.add_member(team_request=get_object_or_404(TeamRequest, pk=value))
    #                 return HttpResponseRedirect("/teams/%s" % team.id)
    #
    #             if request.POST.get("kick"):
    #                 team.kick_member(user=get_object_or_404(UserModel, pk=value))
    #                 return HttpResponseRedirect("/teams/%s" % team.id)
    #
    #             if request.POST.get("refuse"):
    #                 teamreq = get_object_or_404(TeamRequest, pk=value)
    #                 teamreq.delete()
    #                 print("refuse")
    #                 return HttpResponseRedirect("/teams/%s" % team.id)
    #
    #             if request.POST.get("yes"):
    #                 print("yes")
    #                 vote = get_object_or_404(EventVote, pk=value)
    #                 vote.i_go(self.request.user)
    #                 return HttpResponseRedirect("/teams/%s" % team.id)
    #
    #             if request.POST.get("no"):
    #                 vote = get_object_or_404(EventVote, pk=value)
    #                 vote.not_go(self.request.user)
    #                 return HttpResponseRedirect("/teams/%s" % team.id)
    #
    #         return HttpResponseRedirect("/teams/%s" % team.id)


# for key, value in request.POST.items():
#     print('Key: %s' % (key))
#     # print(f'Key: {key}') in Python >= 3.7
#     print('Value %s' % (value))
#     # print(f'Value: {value}') in Python >= 3.7
# for key, value in request.GET.items():
#     print("Get")
#     print('Key: %s' % (key))
#     # print(f'Key: {key}') in Python >= 3.7
#     print('Value %s' % (value))
#     # print(f'Value: {value}') in Python >= 3.7
