from django.urls import path

from .views import (
    EventListView,
    EventDetailView,
    EventByTagsListView,
    EventTagsListView,
    EventPostDeleteView,
    EventTagsDeleteView,
    EventPostCreateView,
    EventUpdateView,
    EventDeleteView
)

app_name = "event"

urlpatterns = [
    # Events links

    path("", EventListView.as_view(), name="events"),
    path("<int:pk>/", EventDetailView.as_view(), name="event"),
    path("<int:pk>/create", EventPostCreateView.as_view(), name="create-post"),
    path("<int:pk>/edit", EventUpdateView.as_view(), name="edit-event"),
    path("<int:pk>/confirm-delete", EventDeleteView.as_view(), name="delete-event"),

    # Tags links

    path("tags/", EventTagsListView.as_view(), name="tags"),
    path("tags/<int:pk>/confirm-delete", EventTagsDeleteView.as_view(), name="delete-tags"),
    path("<event_tags>/", EventByTagsListView.as_view(), name="by_tags"),
    # path("tags/", EventTagsListView.as_view(), name="Tags"),





]


