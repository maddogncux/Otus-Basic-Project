from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import TeamListView,TeamCreate,TeamDetails


app_name = "airsoft_teams"
urlpatterns = [
    path("", TeamListView.as_view(), name="teams"),
    path("create/", TeamCreate.as_view(), name="create"),
    path("<int:pk>/", TeamDetails.as_view(), name="team"),






            ]


