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
        org_member = get_object_or_404(Member, user=user, org=obj)
        Member.set_owner(org_member)
        return HttpResponseRedirect(f"/organization/{obj.id}")


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

    queryset = Organization \
        .objects \
        .prefetch_related("org_request", "org_members", "event_owner") \
        .select_related()

    # Move to user manger  (mby use in include templates?)
    # def get_form_kwargs(self):
    #     kwargs = super(self).get_form_kwargs()
    #     kwargs['request'] = self.request
    #     return kwargs

    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            group = get_object_or_404(Organization, pk=self.kwargs["pk"])
            group.request_handler(request=request, user=self.request.user)
            return HttpResponseRedirect(f"/organization/{group.id}")
