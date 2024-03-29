from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import CreateView, ListView, DetailView

from airsoft_organization.models import Organization, Member
from airsoft_registration.models import EventVote

from .forms import EventCreateForm
from .models import Event


class EventCreateViews(CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = "event_create.html"

    def form_valid(self, form):
        member = get_object_or_404(Member, pk=self.kwargs["pk"], user=self.request.user)
        if Organization.can_create_event(member.org, member):
            obj = form.save(commit=False)
            obj.owner = member.org
            obj.save()
            return HttpResponseRedirect(f'/events/{obj.id}')
        # else:
        #     return HttpResponseRedirect(f'/organization/{self.kwargs["pk"]}')


class EventListVies(ListView):
    paginate_by = 14
    context_object_name = "events"
    template_name = "events.html"
    model = Event
    queryset = Event.objects.all()


class EventDetails(DetailView):
    context_object_name = "event"
    template_name = 'event_details.html'
    queryset = Event.objects.prefetch_related("registered_teams")
    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            for key, value in request.POST.items():
                print(f'Key:{key}', key)
                print(f'Value:{value}', value)
            print(self.kwargs)
            print(self.args)
            event = get_object_or_404(Event, pk=self.kwargs["pk"])
            if request.POST.get("vote"):
                EventVote.objects.get_or_create(event=event,
                                                team=self.request.user.team_profile.team)

                return HttpResponseRedirect(f'/events/{event.id}')
        print(str(event))
        return HttpResponseRedirect(f'/events/{event.id}')
