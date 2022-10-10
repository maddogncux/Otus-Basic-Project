from django.urls import path

from .views import (
    EventListView,
    EventDetailView,
    EventByTagsListView,
    EventTagsListView,
    # EventPostDeleteView,
    EventTagsDeleteView,
    EventPostCreateView,
    EventUpdateView,
    EventDeleteView,
    EventPostUpdateView,
    EventPostDetailView,
    EventPostDeleteView


)


app_name = "event"

urlpatterns = [
    # Events links
    path("<int:pk>/confirm-delete", EventDeleteView.as_view(), name='delete-event'),
    path("<int:pk>/edit", EventUpdateView.as_view(), name="edit-event"),
    path("<int:pk>/", EventDetailView.as_view(), name="event"),
    path("", EventListView.as_view(), name="events"),

    # Tags links

    path("tags/", EventTagsListView.as_view(), name="tags"),
    path("<event_tags>/", EventByTagsListView.as_view(), name="by_tags"),
    path("tags/<int:pk>/confirm-delete", EventTagsDeleteView.as_view(), name="delete-tags"),
    # path("tags/", EventTagsListView.as_view(), name="Tags"),

    # Posts links
    path("<int:pk>/create", EventPostCreateView.as_view(), name="create-post"),
    path("<int:events_pk>/post/<int:pk>/", EventPostDetailView.as_view(), name="post-detail"),
    path("<int:events_pk>/post/<int:pk>/edit_post", EventPostUpdateView.as_view(), name="edit-post"),
    path("<int:events_pk>/post/<int:pk>/confirm-delete", EventPostDeleteView.as_view(), name="delete-post"),
]


