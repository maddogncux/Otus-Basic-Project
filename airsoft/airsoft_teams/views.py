# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from guardian.decorators import permission_required_or_403
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from airsoft_teams.forms import TeamPostForm
from airsoft_teams.models import Team, Team_Member, TeamRequest

UserModel: AbstractUser = get_user_model()


# @method_decorator(login_required, name='dispatch')
class TeamCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "team_create.html"
    model = Team
    success_message = 'Team was create successfully'
    # form_class = TeamCreateForm
    fields = ["name", "city", "description", "chevron", "pattern", "is_private"]

    def form_valid(self, form,):
        user = self.request.user
        team = form.save(commit=False)
        team.save()
        member = Team_Member.objects.create(user=user, team=team)
        form.save_m2m()
        self.request.user.team_profile.set_owner()
        return HttpResponseRedirect("/teams/%s" % team.id)


class TeamListView(ListView):
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = Team.objects.order_by('-created_at')




class TeamDetails(DetailView):
    # class TeamDetails(DetailView):
    template_name = 'team_details.html'
    model = Team


class TeamMemberDetails(DetailView):
    template_name = 'team_member_details.html'
    context_object_name = "member"
    model = Team_Member


# @permission_required_or_403("airsoft.g_view_team",)
class TeamMemberDetails(PermissionRequiredMixin, DetailView):
    # class TeamMemberDetails(DetailView):
    template_name = 'team_member_details.html'
    model = Team
    permission_required = ['g_view_team']
    raise_exception = True
    queryset = Team \
        .objects \
        .prefetch_related("team_request",
                          "event_vote",
                          "team_member",
                          "team_registration",
                          "team_post") \
        .select_related()

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.team = None

    # def get_queryset(self, *args, **kwargs):
    #     self.team = get_object_or_404(Team, name=self.kwargs['pk'])
    #     return self.team
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.object)
        context['post_form'] = TeamPostForm()
        # context['self_member'] = Members.objects.filter(user=self.request.user, team=self.object)
        return context

    # def post(self, request, *args, **kwargs, ):
    #     if request.method == 'POST':
    #         team = get_object_or_404(Team, pk=self.kwargs["pk"])
    #         print("iam_here")
    #         team.request_handler(request=request, user=self.request.user)
    #         return HttpResponseRedirect("/teams/%s" % team.id)


class PostCreateView(CreateView, PermissionRequiredMixin):
    template_name = "team_post_create.html"
    form_class = TeamPostForm

    def form_valid(self, form):
        team = self.request.user.team_profile.team
        print(team)
        user = self.request.user
        if user.has_perm("g_create_team_post", user.team_profile.team):
            obj = form.save(commit=False)
            obj.created_by = user
            obj.team = team
            obj.save()
            return HttpResponseRedirect("/teams/%s" % team.id)
        else:
            print("no perm")
            return HttpResponseRedirect("/teams/%s" % user.team_profile.team.id)


def member_manager(request, team_pk, member_pk):
    print(member_pk, team_pk)
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(request.POST.items())
            print("i am dumb")
            print(key)
            print(value)
        get_object_or_404(Team_Member, pk=member_pk).request_handler(key, value)
        return HttpResponseRedirect("/teams/%s" % team_pk)


def request_manager(request, team_pk, request_pk):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(request.POST.items())
        get_object_or_404(TeamRequest, pk=request_pk).request_handler(key, value)
        return HttpResponseRedirect("/teams/%s" % team_pk)

# def form_valid(self, form):

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
