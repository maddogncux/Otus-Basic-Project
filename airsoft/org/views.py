from django.urls import reverse, reverse_lazy

from .models import Organizations
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrgForm
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)


# Create your views here.


class OrgCreateView(LoginRequiredMixin, CreateView):
    model = Organizations
    form_class = OrgForm
    success_url = reverse_lazy("org:orgs")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)



class OrgListView(ListView):
    context_object_name = "Organization"
    queryset = (Organizations
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class OrgDetailView(DetailView):
    context_object_name = "org"
    queryset = (Organizations
                .objects
                .select_related("owner")
                # .prefetch_related("events")
                )


# class OrgUpdateView(UpdateView):
#     model = Organization
#     fields = ["name", "city", "Description"]
#     template_name_suffix = '_update_form'
#
#
# class OrgDeleteView(DeleteView):
#     model = Organization


