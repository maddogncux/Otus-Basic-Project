import django.urls
from .views import EventListVies, EventDetails
from airsoft_registration.views import TeamRegistrationView
app_name = "airsoft_event"
urlpatterns = [
    # path("create/", EventCreateViews.as_view(), name="create_event"),
    # path("create/", EventCreateViews.as_view(), include("airsoft_organization.urls")),
    django.urls.path("", EventListVies.as_view(), name="events"),
    django.urls.path("<int:pk>", EventDetails.as_view(), name="event"),
    django.urls.path("<int:pk>/registration", TeamRegistrationView.as_view(), name="team_reg"),  # airsoft_registration


        ]