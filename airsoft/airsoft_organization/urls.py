

from django.urls import path

from airsoft_event.views import EventCreateViews
from .views import OrgListView, OrgCreate, OrgDetails

app_name = "airsoft_organization"
urlpatterns = [
    path("", OrgListView.as_view(), name="orgs"),
    path("create/", OrgCreate.as_view(), name="org_create"),
    path("<int:pk>/", OrgDetails.as_view(), name="org_details"),
    path("<int:pk>/create/", EventCreateViews.as_view(), name="create_event"),


    ]
