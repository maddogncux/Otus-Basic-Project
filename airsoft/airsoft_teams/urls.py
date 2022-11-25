from django.urls import path

from .views import TeamListView, TeamDetailView


app_name = "airsoft_teams"
urlpatterns = [
    path("", TeamListView.as_view(), name="teams"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team_detail"),







            ]


