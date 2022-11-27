
from django.urls import path

from .views import IndexView
from airsoft_membership.views import GroupCreatView,GroupDetailView

app_name = "homepage"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),





            ]
