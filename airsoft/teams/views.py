from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse


from .models import Teams, MemberRequests
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import TeamsForm, MemberRequestsForm, MemberForm
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)

UserModel: AbstractUser = get_user_model()
# Create your views here.
# Team views

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Teams
    form_class = TeamsForm
    success_url = reverse_lazy("teams:teams")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class TeamListView(ListView):
    context_object_name = "teams"
    queryset = (Teams
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class TeamDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "team"
    queryset = (Teams
                .objects
                # .select_related("request_list")
                .prefetch_related("request_list", "registered_team")
                )


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Teams
    fields = ["name", "city", "Description", "members"]
    template_name_suffix = '_update_form'


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Teams


# Teams members views

class MemberRequestsView(CreateView, LoginRequiredMixin):
    model = MemberRequests
    form_class = MemberRequestsForm

    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Teams, slug=self.kwargs['slug'])
        user = self.request.user
        if user not in team.members.all():
            if user != team.owner:
                member_request = MemberRequests.objects.create(team=team, user=user, request_text="some text")
                member_request.save()
            else:
                return HttpResponseRedirect("/teams/%s" % team.slug)
            return HttpResponseRedirect("/teams/%s" % team.slug)
        else:
            return HttpResponseRedirect("/teams/%s" % team.slug)


        # return reverse("teams:team", kwargs={"slug": self.kwargs['slug']})

    # def form_valid(self, form):
    #     print(self.kwargs)
    #     obj = form.save(commit=False)
    #     obj.user = self.request.user
    #     obj.team = get_object_or_404(Teams, slug=self.kwargs['slug'])
    #     obj.save()
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("teams:team", kwargs={"slug": self.kwargs['slug']})


class AddMember(PermissionRequiredMixin, UpdateView):
    model = MemberRequests
    form_class = MemberForm
    permission_required ='teams.add_members'


    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Teams, slug=self.kwargs['slug'])
        user = get_object_or_404(MemberRequests, pk=self.kwargs['pk']).user
        team.members.add(user)
        team.save()
        del_request = get_object_or_404(MemberRequests, pk=self.kwargs["pk"])
        del_request.delete()
        return HttpResponseRedirect("/teams/%s" % team.slug)

    # member through="Members"
    # def post(self, request, *args, **kwargs):
    #     user = get_object_or_404(MemberRequests, pk=self.kwargs['pk']).user
    #     team = get_object_or_404(Teams, slug=self.kwargs['slug'])
    #     user.member.team = get_object_or_404(Teams, slug=self.kwargs['slug'])
    #     user.member.save()
    #     del_request = get_object_or_404(MemberRequests, pk=self.kwargs["pk"])
    #     del_request.delete()
    #     return HttpResponseRedirect("/teams/%s" % team.slug)


class LeaveTeam(UpdateView, LoginRequiredMixin):
    model = Teams
    form_class = TeamsForm
    #work without get_object
    def get_object(self, queryset=None):
        return Teams.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        user = self.request.user
        team = get_object_or_404(Teams, slug=self.kwargs['slug'])
        team.members.remove(user)
        team.save()
        return HttpResponseRedirect("/teams/%s" % team.slug)


class KickMember(UpdateView, LoginRequiredMixin):
    model = Teams
    form_class = TeamsForm

    # work once without get_object
    def get_object(self, queryset=None):
        return Teams.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Teams, slug=self.kwargs['slug'])
        user = UserModel.objects.get(pk=self.kwargs['pk'])
        owner = self.request.user
        if owner == team.owner:
            team.members.remove(user)
            team.save()
            return HttpResponseRedirect("/teams/%s" % team.slug)
        else:
            # must be message
            HttpResponseRedirect("/teams/%s" % team.slug)



    # def post(self, request, *args, **kwargs):
    #     team = get_object_or_404(Teams, slug=self.kwargs['slug'])
    #     user = UserModel.objects.get(pk=self.kwargs['pk'])
    #     team.members.remove(user)
    #     team.save()
    #     return HttpResponseRedirect("/teams/%s" % team.slug)

        # if owner is team.owner:
        #     user = get_object_or_404(UserModel, pk=self.kwargs['id'])
        #     user.member.team = None
        #     user.member.save()
        #     return HttpResponseRedirect("/teams/%s" % team.slug)
        # else:
        #     return HttpResponseRedirect("/teams/%s" % team.slug)









        # member = get_object_or_404(MemberRequests, pk=self.kwargs['pk']).user.member
        # member.team = get_object_or_404(Teams, slug=self.kwargs['slug'])
        # member.save()
        # instance = get_object_or_404(MemberRequests, pk=self.kwargs["pk"])
        # instance.delete()
        # request = get_object_or_404(MemberRequests, pk=self.kwargs['pk'])
        # request.user.member.team = (get_object_or_404(Teams, slug=self.kwargs['slug']))
        # request.user.member.save()
        #
        # request.delete()
        # return reverse("teams:team", kwargs={"slug": self.kwargs['slug']})



    #         object = super().post(request, **kwargs)
    #         team = Team.objects.get(pk=kwargs["pk"])
    #         players = Player.objects.filter(user_id__in=self.request.POST.get("tags").split(","))
    #         team.players.set(players)
    #         team.save()
    #         return object




    # def form_valid(self, form):
    #     print(self.kwargs)
    #     print(self.args)
    #     form = form.save(commit=False)
    #     form.team = self.request.user.team_owner
    #     form.save()
    #     # instance = get_object_or_404(UserModel, pk=self.kwargs["pk"])  # will not work with many users its w
    #     # instance.delete()
    #
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("teams:team", kwargs={"slug": self.kwargs['slug']})










# class MakeMemberView(CreateView, LoginRequiredMixin):
#     model = Members
#     form_class = MemberAddForm
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         print(self.kwargs)
#         print(self.args)
#         # request = get_object_or_404(MemberRequests, pk=self.kwargs["pk"])
#         print(self.team)
#         obj.user = get_object_or_404(MemberRequests, pk=self.kwargs["pk"]).user
#         # obj.user = request.user
#         obj.team = get_object_or_404(MemberRequests, pk=self.kwargs["pk"]).team
#         # obj.team = request.team
#         obj.save()
#         # instance = get_object_or_404(MemberRequests, pk=self.kwargs["pk"])
#         # instance.delete()
#
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("teams:team", kwargs={"slug": self.kwargs['slug']})
#
#
#
#
#
#
#
# class AddMember2(UpdateView):
#     models = Teams
#     form_class = TeamsForm
#
#     def form_valid(self, form):
#         print(self.kwargs)
#         if self.request.user.id == self.team.owner.id:
#             form = form.save(commit=False)
#             form.member = (get_object_or_404(UserModel, pk=self.kwargs["pk"]))
#             form.save()
#             return super().form_valid(form)
#         else:
#             print(self.kwargs)
#
#
#
#























    # model = Teams
    # form_class = TeamsForm

    # #
    # def post(self, request, *args, **kwargs):
    #     object = super().post(request, **kwargs)
    #     team = Teams.objects.get(slug=self.kwargs['slug'])
    #     team.members.add(get_object_or_404(MemberRequests, pk=self.kwargs["pk"]).user)
    #     team.save
    #     return

    # def get_success_url(self):
    #     return reverse("teams:team", kwargs={"slug": self.object.team.slug})


    # def post(self, request, *args, **kwargs):
    #     object = super().post(request, **kwargs)
# #         team = Team.objects.get(pk=kwargs["pk"])
# #         players = Player.objects.filter(user_id__in=self.request.POST.get("tags").split(","))
# #         team.players.set(players)
# #         team.save()
# #         return object








# if I found it does not mean that I stole

# @method_decorator(decorators, name='dispatch')
# class RequestToTeamView(SuccessMessageMixin, CreateView):
#     model = TeamRequest
#     template_name = "team/request.html"
#     success_message = "Вы "
#
#     def post(self, request, *args, **kwargs):
#         try:
#             TeamRequest.objects.get(player__user__id=request.user.id)
#             return HttpResponse("Вы не можете подать заявку")
#         except TeamRequest.DoesNotExist:
#             if request.user.is_player:
#                 team = Team.objects.get(pk=kwargs["pk"])
#                 player = Player.objects.get(user__id=request.user.id)
#                 request_to_team = TeamRequest.objects.create(team=team, player=player)
#                 request_to_team.save()
#                 return HttpResponseRedirect("/team/%s" % team.pk)
#             else:
#                 return HttpResponse("Вы не можете подать заявку")


# @method_decorator(decorators, name='dispatch')
# class ManagePlayersInTeamView(SuccessMessageMixin, UpdateView):
#     model = Team
#     template_name = "team/invite.html"
#     form_class = TeamApplicationForm
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["team"] = Team.objects.get(owner_id=self.request.user.id)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         object = super().post(request, **kwargs)
#         team = Team.objects.get(pk=kwargs["pk"])
#         players = Player.objects.filter(user_id__in=self.request.POST.get("tags").split(","))
#         team.players.set(players)
#         team.save()
#         return object

# class TeamManagerView(TemplateView):
#     model = MemberRequests
#     template_name = "team/manage.html"
#     success_message = ""
#     form_class = TeamManageForm
#
#     def get_context_data(self, **kwargs):
#         context = super(TeamManagerView, self).get_context_data()
#         orders = MemberRequests.objects.filter(team__owner_id=self.request.user.id)
#         context["orders"] = orders
#         return context
#
#
# class TeamManagerOrdersView(SuccessMessageMixin, BaseUpdateView, TemplateView):
#     model = TeamRequest
#     template_name = "team/manage.html"
#     success_message = ""
#     form_class = TeamManageForm
#
#     def post(self, request, *args, **kwargs):
#         self.object = super(TeamManagerOrdersView, self).post(request, **kwargs)
#         if self.request.user.is_manager:
#             self.team = Team.objects.filter(owner_id=self.request.user.id)
#             return reverse("/team/%s/manage" % self.team.pk)
