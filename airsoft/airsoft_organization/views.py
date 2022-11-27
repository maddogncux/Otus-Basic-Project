from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from airsoft_organization.models import Organization

# Create your views here.

class OrgListView(ListView):
    context_object_name = "teams"
    template_name = "organization.html"
    queryset = (Organization
                .objects
                # .select_related()
                # .prefetch_related()
                .all())
