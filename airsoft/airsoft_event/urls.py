from django.urls import path, include
from .views import EventCreateViews, EventListVies, EventDetails
app_name = "airsoft_event"
urlpatterns = [
    # path("create/", EventCreateViews.as_view(), name="create_event"),
    # path("create/", EventCreateViews.as_view(), include("airsoft_organization.urls")),
    path("", EventListVies.as_view(), name="events"),
    path("<int:pk>", EventDetails.as_view(), name="event"),



        ]