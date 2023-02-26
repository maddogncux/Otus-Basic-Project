""" team view """
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from guardian.decorators import permission_required_or_403
from guardian.mixins import PermissionRequiredMixin

from airsoft_teams.forms import TeamPostForm
from airsoft_teams.models import Team, TeamMember, TeamRequest

UserModel: AbstractUser = get_user_model()


# @method_decorator(login_required, name='dispatch')
class TeamCreate(LoginRequiredMixin, CreateView):
    """ team create  """
    template_name = "team_create.html"
    model = Team
    success_message = 'Team was create successfully'
    # form_class = TeamCreateForm
    fields = ["name", "city", "description", "chevron", "pattern", "is_private"]

    # def form_valid(self, form, ):
    #     user = self.request.user
    #     if Team_Member.objects.filter(pk=user.id) is not None:
    #         raise U_all_ready_in_team_beyaach_Error("some error message")
    #     else:
    #         team = form.save(commit=False)
    #         team.save()
    #         owner = Team_Member.objects.create(user=user, team=team)
    #         owner.set_owner()
    #         return HttpResponseRedirect("/teams/%s" % team.id)

    def form_valid(self, form, ):
        user = self.request.user
        if TeamMember.objects.filter(pk=user.id) is None:
            team = form.save(commit=False)
            team.save()
            owner = TeamMember.objects.create(user=user, team=team)
            owner.set_owner()
            return HttpResponseRedirect(f'/teams/{team.pk}')
        raise PermissionError("some error message")


class TeamListView(ListView):
    """view all team no permission"""
    context_object_name = "teams"
    template_name = "teams.html"
    queryset = Team.objects.order_by('-created_at')
    paginate_by = 14


class TeamDetails(DetailView):
    """view a team info"""
    # class TeamDetails(DetailView):
    template_name = 'team_details.html'
    model = Team

    def post(self, request, *args, **kwargs, ):
        """custom post for send team request team application"""
        if request.method == 'POST':
            team = get_object_or_404(Team, pk=self.kwargs["pk"])
            user = self.request.user
            if user not in team.members.all():
                TeamRequest.objects.get_or_create(team=team, user=user)
                return HttpResponseRedirect("/teams/")
            raise PermissionError("all ready bro all ready ")


# class TeamMemberDetails(DetailView):
#     template_name = 'team_member_details.html'
#     context_object_name = "member"
#     model = Team_Member

class TeamMemberDetails(PermissionRequiredMixin, DetailView):
    """make one more view member/manager rename this to manager """
    # class TeamMemberDetails(DetailView):
    template_name = 'team_member_details.html'
    permission_required = ['g_view_team']
    raise_exception = True
    queryset = Team \
        .objects \
        .prefetch_related("team_request",
                          "team_request__user",
                          "event_vote",
                          "event_vote__yes",
                          "event_vote__no",
                          "team_member",

                          "team_registration",

                          "team_post",
                          "team_post__created_by",
                          ) \
        .select_related()

    def get_context_data(self, *args, **kwargs):
        """post_form for user can create object in Details view"""
        context = super().get_context_data(*args, **kwargs)
        context['post_form'] = TeamPostForm()
        return context

    # def post(self, request, *args, **kwargs, ):
    #     if request.method == 'POST':
    #         team = get_object_or_404(Team, pk=self.kwargs["pk"])
    #         print("iam_here")
    #         team.request_handler(request=request, user=self.request.user)
    #         return HttpResponseRedirect("/teams/%s" % team.id)


class PostCreateView(CreateView):
    """creation a post in team where user are member """
    template_name = "team_post_create.html"
    form_class = TeamPostForm

    # permission_object = None
    # permission_required = ['g_create_team_post']
    def form_valid(self, form):
        user = self.request.user
        if user.has_perm("g_create_team_post", user.team_profile.team):
            obj = form.save(commit=False)
            obj.created_by = user
            obj.team_id = user.team_profile.team.id
            obj.save()
            return HttpResponseRedirect(f'/teams/{user.team_profile.team.id}')
        print("no perm")
        raise PermissionError("cant talk")


@permission_required_or_403('g_team_member_manager', (Team, 'pk', 'team_pk'))
def member_manager(request, team_pk, member_pk):
    """member_manager with request handler"""
    print(member_pk, team_pk)
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(request.POST.items())
            print("i am dumb")
            print(key)
            print(value)
        get_object_or_404(TeamMember, pk=member_pk).request_handler(key, value)
    return HttpResponseRedirect(f'/teams/{team_pk}')


@permission_required_or_403('g_team_member_manager', (Team, 'pk', 'team_pk'))
def request_manager(request, team_pk, request_pk):
    """request_manager with request handler"""
    print("iamdumbtoo")
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(request.POST.items())
        get_object_or_404(TeamRequest, pk=request_pk).request_handler(key, value)
        return HttpResponseRedirect(f'/teams/{team_pk}')

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
