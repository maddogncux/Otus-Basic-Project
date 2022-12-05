
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, DetailView, CreateView

from airsoft_membership.models import BasicGroup
from airsoft_registration.models import EventVote
from airsoft_teams.models import Team, Members

UserModel: AbstractUser = get_user_model()


class TeamCreate(CreateView):
    template_name = "team_create.html"
    # success_url =
    model = Team
    # form_class =
    fields = ["name", "city", "description", "chevron", "pattern", "is_private"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        user = self.request.user
        obj.members.add(user)
        form.save_m2m()
        mem = get_object_or_404(Members,user=user, team=obj)
        Members.set_owner(mem)
        return super().form_valid(form)


class TeamListView(ListView):
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = (Team
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class TeamDetails(DetailView):
    template_name = 'team_details.html'
    queryset = Team.objects.prefetch_related("event_vote")


    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            print("get post")
            for key, value in request.POST.items():
                print("chek keys")
                print('Key: %s' % (key))
                print('Value %s' % (value))
            group = get_object_or_404(BasicGroup, pk=self.kwargs["pk"])
            print("get groupe")
            if request.POST.get("add_request"):
                print("add_request")
                BasicGroup.add_request(group, user=self.request.user)
                return HttpResponseRedirect("/teams/%s" % group.id)
            else:

                if request.POST.get("add"):
                    member = get_object_or_404(UserModel, pk=value)
                    print("add")
                    BasicGroup.add_member(group,  member)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("kick"):
                    member = get_object_or_404(UserModel, pk=value)
                    print("kick")
                    BasicGroup.kick_member(group, member)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("refuse"):
                    member = get_object_or_404(UserModel, pk=value)
                    print("refuse")
                    BasicGroup.refuse_request(group, member)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("yes"):
                    print("yes")
                    vote = get_object_or_404(EventVote, pk=value)
                    print(vote)
                    user = self.request.user
                    print(user)
                    EventVote.i_go(vote, user)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("no"):
                    print("no")
                    vote = get_object_or_404(EventVote, pk=value)
                    print(vote)
                    user = self.request.user
                    print(user)
                    EventVote.not_go(vote, user)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("vote_reg"):
                    print("vote_reg")
                    vote = get_object_or_404(EventVote, pk=value)
                    EventVote.vote_registration(vote, side)
                    return HttpResponseRedirect("/teams/%s" % group.id)
                
            return HttpResponseRedirect("/teams/%s" % group.id)


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