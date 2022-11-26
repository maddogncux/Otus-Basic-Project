from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from airsoft_teams.models import Team
from airsoft_organization.models import Organization
from .models import BasicGroup, MembershipRequest
from django.views.generic import CreateView, UpdateView
from .forms import BasicGroupForms

# Create your views here.

UserModel: AbstractUser = get_user_model()

class CreateTeamView(CreateView, LoginRequiredMixin):
    model = BasicGroup
    form_class = BasicGroupForms
    reverse_lazy = "/"
    # template_name = "create"


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = BasicGroupForms(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner = self.request.user
                obj.save()
                if request.POST.get("team"):
                    team = Team.objects.create(user_group=obj)
                    team.save()
                    return HttpResponseRedirect("/teams/%s" % team.pk)
                if request.POST.get("organization"):
                    org = Organization.objects.create(user_group=obj)
                    org.save()
                    return HttpResponseRedirect("/teams/%s" % org.pk)
                if request.POST.get("shop"):
                    shop = Organization.objects.create(user_group=obj)
                    shop.save()
                    return HttpResponseRedirect("/")

                else:
                    return HttpResponseRedirect('/')
            else:
                form = BasicGroupForms()
        else:
            return HttpResponseRedirect('/')














































# make simpl way and make check's in templates members\owner and don't show button
# moved to detail view teams

class CreateRequest(CreateView, LoginRequiredMixin):
    model = MembershipRequest
    fields = []
    def post(self, request, *args, **kwargs):
        # group = get_object_or_404(BasicGroup, pk=self.kwargs['pk'])
        # MembershipRequest.objects.create(group=group, user=self.request.user)

        group = get_object_or_404(BasicGroup, pk=self.kwargs['pk'])
        user = self.request.user
        if user not in group.members.all():
            if user != group.owner:
                member_request = MembershipRequest.objects.create(group=group, user=user)
                member_request.save()
            else:
                return HttpResponseRedirect("/teams/%s" % group.pk)
            return HttpResponseRedirect("/teams/%s" % group.pk)
        else:
            return HttpResponseRedirect("/teams/%s" % group.pk)



class AddRequestByUser(UpdateView, LoginRequiredMixin):
    model = BasicGroup
    fields = []

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     user = self.request.user
    #     if user not in obj.members.all():
    #         if user != obj.owner:
    #             obj.request_user = user
    #             obj.save()
    #             return HttpResponseRedirect("/teams/%s" % group.pk)
    #     return HttpResponseRedirect("/teams/%s" % group.pk)


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get("add_requsete"):
                group = get_object_or_404(BasicGroup, pk=self.kwargs["pk"])
                user_request = self.request.user
                self.object.add_requsete(user_request)



