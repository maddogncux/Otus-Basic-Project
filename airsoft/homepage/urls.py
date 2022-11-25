
from django.urls import path

from .views import IndexView
from airsoft_membership.views import CreateTeamView

app_name = "homepage"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('create/', CreateTeamView.as_view(), name="create"),
]
