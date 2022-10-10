from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView,
                                  DetailView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView,
                                  )

from teams.models import Teams
from .forms import EventForms
from .forms import EventPostForms
from .models import (Event,
                     EventTags,
                     EventPost,
                     AdditionalServices,
                     Sides,
                     RegisteredTeams,
                     EventReg,
                     )


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForms
    success_url = reverse_lazy("event:events")

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.owner = get_object_or_404(Organizations, slug=self.kwargs['slug'])
        obj.owner = self.request.user.organization
        obj.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.event = get_object_or_404(Event, slug=self.kwargs['slug'])
    #     post.save()
    #     return super(EventPostCreateView, self).form_valid(form)


class EventListView(ListView):
    context_object_name = "events"
    queryset = (Event
                .objects
                # .select_related("tags")
                .prefetch_related("post", "tags")
                .all())


class EventDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "event"
    queryset = (Event
                .objects
                # .select_related()
                .prefetch_related("post", "tags")
                )


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForms
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.object.slug})


class EventDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = "delete"
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


class EventTagsDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = "tag"
    model = EventTags
    success_url = reverse_lazy("event:tags")


class EventPostCreateView(CreateView):
    model = EventPost
    form_class = EventPostForms

    def form_valid(self, form):
        post = form.save(commit=False)
        post.event = get_object_or_404(Event, slug=self.kwargs['slug'])
        post.save()
        return super(EventPostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.object.event.slug})  # Optimize


class EventPostDetailView(DetailView):
    context_object_name = "post"
    model = EventPost


class EventPostUpdateView(LoginRequiredMixin, UpdateView):
    model = EventPost
    fields = ["name", "body"]
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.object.event.slug})  # Optimize


class EventPostDeleteView(LoginRequiredMixin, DeleteView):
    model = EventPost

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.object.event.slug})  # Optimize


class AddServicesCreateView(CreateView):
    model = AdditionalServices
    fields = ["service", "price"]

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.object.event.slug})


class SidesCreateView(CreateView):
    model = Sides
    fields = ["event", "side"]


class RegTeam(CreateView):
    model = RegisteredTeams
    fields = ["side", "addservice"]

    # form_class = RegisteredTeams

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.registration = get_object_or_404(Event, slug=self.kwargs['slug']).event_reg
        obj.team = self.request.user.team_owner
        obj.save()
        return super(RegTeam, self).form_valid(form)

    def get_success_url(self):
        return reverse("event:event", kwargs={"slug": self.kwargs['slug']})


# must one class with post(yes\no\mby)
class Yes(UpdateView):
    model = RegisteredTeams
    fields = []

    def get_object(self, queryset=None):
        return RegisteredTeams.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.request.user
        team = Teams.objects.get(slug=self.kwargs['slug'])
        reg = RegisteredTeams.objects.get(pk=self.kwargs['pk'])
        reg.yes.add(user)
        reg.mby.remove(user)
        reg.no.remove(user)
        reg.save()
        return HttpResponseRedirect("/teams/%s" % team.slug)

    # must one class with post(yes\no\mby)


class No(UpdateView):
    model = RegisteredTeams
    fields = []

    def get_object(self, queryset=None):
        return RegisteredTeams.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.request.user
        team = Teams.objects.get(slug=self.kwargs['slug'])
        reg = RegisteredTeams.objects.get(pk=self.kwargs['pk'])
        reg.no.add(user)
        reg.yes.remove(user)
        reg.no.remove(user)
        reg.save()
        return HttpResponseRedirect("/teams/%s" % team.slug)

    # must one class with post(yes\no\mby)


class Mby(UpdateView):
    model = RegisteredTeams
    fields = []

    def get_object(self, queryset=None):
        return RegisteredTeams.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.request.user
        team = Teams.objects.get(slug=self.kwargs['slug'])
        reg = RegisteredTeams.objects.get(pk=self.kwargs['pk'])
        reg.mby.add(user)
        reg.no.remove(user)
        reg.yes.remove(user)
        reg.save()
        return HttpResponseRedirect("/teams/%s" % team.slug)


class ApplyRegistration(UpdateView):
    model = RegisteredTeams
    fields = []

    # pk_url_kwarg = "reg_pk"
    #
    # def get_object(self, queryset=None):
    #     obj = super().get_object()
    #     # obj = RegisteredTeams.objects.get(pk=self.kwargs['pk'])
    #     # return RegisteredTeams.objects.get(pk=self.kwargs['pk'])
    #     # return obj

    def post(self, request, *args, **kwargs):
        team = Teams.objects.get(slug=self.kwargs['slug'])
        reg = RegisteredTeams.objects.get(pk=self.kwargs['pk'])
        owner = self.request.user

        # reg.registration_send = True
        # reg.save()
        # return HttpResponseRedirect("/teams/%s" % team.slug)

        if owner == team.owner:
            if not reg.registration_send:
                reg.registration_send = True
                reg.save()
                return HttpResponseRedirect("/teams/%s" % team.slug)
            else:
                reg.registration_send = False
                reg.save()
                return HttpResponseRedirect("/teams/%s" % team.slug)
        else:
            return HttpResponseRedirect("/teams/%s" % team.slug)


class RegView(DetailView):
    queryset = (EventReg
                .objects
                .prefetch_related("registered"))

    context_object_name = "regs"

    # def get(self, request, *args, **kwargs):
    #    return EventReg.objects.get(pk=self.kwargs['pk'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["regs"] = EventReg.objects.get(pk=self.kwargs['pk'])
    #     return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(registered__registration_send=True)

    # def get_object(self, queryset=None):
    #     return EventReg.objects.get(pk=self.kwargs['pk'])
