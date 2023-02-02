from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView


from airsoft_organization.models import Organization, Member

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
        change_role = get_object_or_404(Member, user=user, team=obj)
        Member.set_owner(change_role)
        return HttpResponseRedirect("/organization/%s" % obj.id)


class OrgListView(ListView):
    paginate_by = 14
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
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given team"""
        kwargs = super(self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            group = get_object_or_404(Organization, pk=self.kwargs["pk"])
            if request.POST.get("add_requsete"):
                Organization.add_request(group, user=self.request.user)
                return HttpResponseRedirect("/teams/%s" % group.id)
            else:
                member = get_object_or_404(UserModel, pk=self.kwargs["value"])
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
