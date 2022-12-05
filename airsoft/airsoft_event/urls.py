from django.urls import path, include
from .views import EventListVies, EventDetails
from airsoft_registration.views import TeamRegistrationView
app_name = "airsoft_event"
urlpatterns = [
    # path("create/", EventCreateViews.as_view(), name="create_event"),
    # path("create/", EventCreateViews.as_view(), include("airsoft_organization.urls")),
    path("", EventListVies.as_view(), name="events"),
    path("<int:pk>", EventDetails.as_view(), name="event"),
    path("<int:pk>/registration", TeamRegistrationView.as_view(), name="team_reg"),  # airsoft_registration


        ]