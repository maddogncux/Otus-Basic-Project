from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .models import Event, EventTags, EventPost



class EventListView(ListView):
    template_name = "event/events.html"
    context_object_name = "events"
    queryset = (Event
                .objects
                # .select_related("tags")
                .prefetch_related("post", "tags")
                .all())


class EventDetailView(DetailView):
    context_object_name = "event"
    queryset = (Event
                .objects
                # .select_related()
                .prefetch_related("post", "tags")
                )


class EventUpdateView(UpdateView):
    model = Event
    fields = ["name", "place", "duration", "body", "additional_block1"]
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("event:event", kwargs={"pk": self.object.pk})


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy("event:events")



class EventTagsListView(ListView):
    model = EventTags
    success_url = reverse_lazy("event:tags")

class EventByTagsListView(ListView):
    template_name = "event/events.html"
    queryset = Event.objects.prefetch_related("tags")

    def get_queryset(self):
        qs = super().get_queryset()
        tags_name = self.kwargs["event_tags"]
        tags: EventTags = get_object_or_404(EventTags, name=tags_name)
        return qs.filter(tags=tags)


class EventTagsDeleteView(DeleteView):
    context_object_name = "tag"
    model = EventTags
    success_url = reverse_lazy("event:tags")


class EventPostCreateView(CreateView):
    model = EventPost
    fields = ["name", "body"]

    def form_valid(self, form):
        form.instance.event_id = self.kwargs['pk']
        return super(EventPostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("event:event", kwargs={"pk": self.object.event.pk})


class EventPostDeleteView(DeleteView):
    model = EventPost


