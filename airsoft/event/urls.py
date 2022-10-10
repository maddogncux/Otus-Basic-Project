from django.conf import settings
from django.conf.urls.static import static
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
    EventPostDeleteView,
    # EventCreateView,
    AddServicesCreateView,
    SidesCreateView,
    RegTeam,
    RegView,

)


app_name = "event"

urlpatterns = [
    # Events links
    # path('create/', EventCreateView.as_view(), name="create"),
    path("<slug:slug>/delete", EventDeleteView.as_view(), name='delete'),
    path("<slug:slug>/edit", EventUpdateView.as_view(), name="edit"),
    path("<slug:slug>/", EventDetailView.as_view(), name="event"),
    path("", EventListView.as_view(), name="events"),

    # Tags links

    path("tags/", EventTagsListView.as_view(), name="tags"),
    path("<event_tags>/", EventByTagsListView.as_view(), name="by_tags"),
    path("tags/<int:pk>/confirm-delete", EventTagsDeleteView.as_view(), name="delete-tags"),
    # path("tags/", EventTagsListView.as_view(), name="Tags"),

    # Posts links
    path("<slug:slug>/create", EventPostCreateView.as_view(), name="create-post"),
    path("<slug:slug>/post/<int:pk>/", EventPostDetailView.as_view(), name="post-detail"),
    path("<slug:slug>/post/<int:pk>/edit_post", EventPostUpdateView.as_view(), name="edit-post"),
    path("<slug:slug>/post/<int:pk>/confirm-delete", EventPostDeleteView.as_view(), name="delete-post"),
    #
    path("<slug:slug>/services", AddServicesCreateView.as_view(), name="services"),
    path("<slug:slug>/sides", SidesCreateView.as_view(), name="sides"),
    path("<slug:slug>/reg", RegTeam.as_view(), name="reg"),
    path("<slug:slug>/reginfo/<int:pk>", RegView.as_view(), name="reg-detail"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


