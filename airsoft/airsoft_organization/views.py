from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView


from airsoft_organization.models import Organization, Member, OrgRequest

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
        org_member = get_object_or_404(Member, user=user, team=obj)
        Member.set_owner(org_member)
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
    # model = Organization
    queryset = Organization\
        .objects\
        .prefetch_related("org_request")\
        .select_related()
    # Move to user manger  (mby use in include templates?)
    def get_form_kwargs(self):
        kwargs = super(self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            group = get_object_or_404(Organization, pk=self.kwargs["pk"])
            group.request_handler(request=request, user=self.request.user)
            return HttpResponseRedirect("/organization/%s" % group.id)
        return HttpResponseRedirect("/organization/%s" % group.id)

    # def post(self, request, *args, **kwargs, ):
    #     if request.method == 'POST':
    #         for key, value in request.POST.items():
    #             print(request.POST.items())
    #             print("check keys")
    #             print('Key: %s' % (key))
    #             print('Value %s' % (value))
    #         group = get_object_or_404(Organization, pk=self.kwargs["pk"])
    #         if request.POST.get("add_request"):
    #             group.send_request(user=self.request.user)
    #             return HttpResponseRedirect("/organization/%s" % group.id)
    #         if request.POST.get("add"):
    #
    #             group.add_member(org_request=get_object_or_404(OrgRequest, pk=value))
    #             return HttpResponseRedirect("/organization/%s" % group.id)
    #         if request.POST.get("refuse"):
    #             group.refuse_request(org_request=get_object_or_404(OrgRequest, pk=value))
    #
    #
    #     return HttpResponseRedirect("/organization/%s" % group.id)

