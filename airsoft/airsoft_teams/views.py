
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
        user_in_team = Team.objects.filter(members=user)
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
        .prefetch_related("team_request", "event_vote", "team_members")\
        .select_related()






    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            print("get post")
            for key, value in request.POST.items():
                print("check keys")
                print('Key: %s' % (key))
                print('Value %s' % (value))
            team = get_object_or_404(Team, pk=self.kwargs["pk"])
            print("get group")
            if request.POST.get("add_request"):
                print("add_request")
                Team.send_request(team, user=self.request.user)
                return HttpResponseRedirect("/teams/%s" % team.id)
            else:
                # if request.POST.get("add"):
                #     user = get_object_or_404(UserModel, pk=value)
                #     print("add")
                #     Team.add_member(team, user)
                #     return HttpResponseRedirect("/teams/%s" % team.id)
                if request.POST.get("add"):
                    team_request = get_object_or_404(TeamRequest, pk=value)
                    print("add")
                    Team.add_member(team_request.team, team_request)
                    return HttpResponseRedirect("/teams/%s" % team.id)

                if request.POST.get("kick"):
                    user = get_object_or_404(UserModel, pk=value)
                    print("kick")
                    Team.kick_member(team, user)
                    return HttpResponseRedirect("/teams/%s" % team.id)

                if request.POST.get("refuse"):
                    teamreq = get_object_or_404(TeamRequest, pk=value)
                    teamreq.delete()
                    print("refuse")
                    # Team.refuse_request(team, user)
                    return HttpResponseRedirect("/teams/%s" % team.id)

                if request.POST.get("yes"):
                    print("yes")
                    vote = get_object_or_404(EventVote, pk=value)
                    print(vote)
                    user = self.request.user
                    print(user)
                    EventVote.i_go(vote, user)
                    return HttpResponseRedirect("/teams/%s" % team.id)

                if request.POST.get("no"):
                    print("no")
                    vote = get_object_or_404(EventVote, pk=value)
                    print(vote)
                    user = self.request.user
                    print(user)
                    EventVote.not_go(vote, user)
                    return HttpResponseRedirect("/teams/%s" % team.id)

                if request.POST.get("vote_reg"):
                    print("vote_reg")
                    vote = get_object_or_404(EventVote, pk=value)
                    EventVote.vote_registration(vote, side)
                    return HttpResponseRedirect("/teams/%s" % team.id)
                
            return HttpResponseRedirect("/teams/%s" % team.id)


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