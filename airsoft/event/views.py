from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .models import Event, EventTags, EventPost


# Create your views here.

# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.views.generic.base import TemplateView
# from django.utils.decorators import method_decorator
#
# class IndexView(TemplateView):
#     template_name = 'index.html'
#
#     @method_decorator(ensure_csrf_cookie)
#     def dispatch(self, *args, **kwargs):
#         return super(IndexView, self).dispatch(*args, **kwargs)


# class EventView(View):
#     template_name = "event/index.html"
#     return HttpResponse('Hello, World!')


# def index(request: HttpRequest):
#
#     return render(request=request, template_name="event/index.html", )


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

    # success_url = reverse_lazy("event:event")

    # def form_valid(self, form):
    #     form.instance.event_id = self.kwargs['pk']
    #     return super(EventPostCreateView, self).form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse("event:event", kwargs={"pk": self.object.vent.pk})




class EventTagsListView(ListView):
    model = EventTags


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


