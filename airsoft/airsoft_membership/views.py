from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from airsoft_teams.models import Team
from airsoft_organization.models import Organization
from .models import BasicGroup, MembershipRequest
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import BasicGroupForms

# Create your views here.

UserModel: AbstractUser = get_user_model()

class GroupCreatView(CreateView, LoginRequiredMixin):
    model = BasicGroup
    form_class = BasicGroupForms
    reverse_lazy = "/"
    # template_name = "create"

    # mby split on different function or move to models
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



class GroupDetailView(DetailView):
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



