from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView

from airsoft_membership.models import BasicGroup
from airsoft_organization.models import Organization

# Create your views here.

UserModel: AbstractUser = get_user_model()


class OrgCreate(CreateView):
    template_name = "organization_create.html"
    context_object_name = "org"
    # success_url =
    model = Organization
    # form_class =
    fields = ["name", "city", "description", "logo", "is_private"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.membership = BasicGroup.objects.create()
        obj.save()
        return super().form_valid(form)


class OrgListView(ListView):
    context_object_name = "orgs"
    template_name = "organizations.html"
    queryset = (Organization
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class OrgDetails(DetailView):
    template_name = 'organization_details.html'
    context_object_name = "org"
    model = Organization

    # Move to user manger  (mby use in include templates?)
    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            group = get_object_or_404(BasicGroup, pk=self.kwargs["pk"])
            if request.POST.get("add_requsete"):
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
        return HttpResponseRedirect("/teams/%s" % group.id)
