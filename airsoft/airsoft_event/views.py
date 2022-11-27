from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import CreateView

from airsoft_organization.models import Organization
from .forms import EventCreateForm
from .models import Event


class EventCreateViews(CreateView):
    model = Event
    form_class = EventCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = get_object_or_404(Organization, pk=self.kwargs['pk'])
        obj.save()
        return super().form_valid(form)

