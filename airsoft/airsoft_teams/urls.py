from django.urls import path

from .views import TeamListView


app_name = "airsoft_teams"
urlpatterns = [
    path("", TeamListView.as_view(), name="teams"),








            ]


