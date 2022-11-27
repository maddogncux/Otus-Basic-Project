app_name = "airsoft_organization"

from django.urls import path

from .views import OrgListView

app_name = "airsoft_organization"
urlpatterns = [
    path("", OrgListView.as_view(), name="orgs"),


    ]