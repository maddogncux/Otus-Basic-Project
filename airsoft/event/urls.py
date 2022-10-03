from django.urls import path

from .views import (
    EventListView,
    EventDetailView,
    EventByTagsListView,
    EventTagsListView,
    EventPostDeleteView,
    EventTagsDeleteView,
    EventPostCreateView
)

app_name = "event"

urlpatterns = [
    # path("", index,app_name="index")
    path("", EventListView.as_view(), name="events"),
    path("tags/", EventTagsListView.as_view(), name="tags"),
    path("tags/<int:pk>/confirm-delete", EventTagsDeleteView.as_view(), name="delete-tags"),
    path("<int:pk>/", EventDetailView.as_view(), name="event"),
    path("<int:pk>/create", EventPostCreateView.as_view(), name="create-post"),
    # path("<int:pk>/", EventUpdateView.as_view(), name="edit"),
    # path("tags/", EventTagsListView.as_view(), name="Tags"),
    path("<event_tags>/", EventByTagsListView.as_view(), name="by_tags"),




]


