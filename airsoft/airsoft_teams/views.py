
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, DetailView, CreateView

from airsoft_membership.models import BasicGroup
from airsoft_teams.models import Team

UserModel: AbstractUser = get_user_model()


class TeamCreate(CreateView):
    template_name = "team_create.html"
    # success_url =
    model = Team
    # form_class =
    fields = ["name", "city", "description", "chevron", "pattern", "is_private"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        membership = BasicGroup.objects.create()
        obj.owner = self.request.user
        obj.membership = membership
        obj.save()
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
    model = Team

    # Move to user manger  (mby use in include templates?)
    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            group = get_object_or_404(BasicGroup, pk=self.kwargs["pk"])
            if request.POST.get("add_request"):
                BasicGroup.add_request(group, user=self.request.user)
                return HttpResponseRedirect("/teams/%s" % group.id)
            else:
                member = get_object_or_404(UserModel, pk=value)
                if request.POST.get("add"):
                    BasicGroup.add_member(group,  member)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("kick"):
                    BasicGroup.kick_member(group, member)
                    return HttpResponseRedirect("/teams/%s" % group.id)

                if request.POST.get("refuse"):
                    BasicGroup.refuse_request(group, member)
                    return HttpResponseRedirect("/teams/%s" % group.id)
            # return HttpResponseRedirect("/teams/%s" % group.id)


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