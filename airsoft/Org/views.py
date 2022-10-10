from django.shortcuts import render
from django.views.generic import DetailView

fr
# Create your views here.


class OrganiztionDetailView(DetailView):
    context_object_name = "event"
    queryset = (Event
                .objects
                # .select_related()
                # .prefetch_related()
                )