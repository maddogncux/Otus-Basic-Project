# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.urls import path

from . import views
from .views import TeamListView, TeamCreate, TeamDetails, PostCreateView, TeamMemberDetails

app_name = "airsoft_teams"
urlpatterns = [
    path("", TeamListView.as_view(), name="teams"),
    path("create/", TeamCreate.as_view(), name="create"),
    path("<int:pk>/", TeamMemberDetails.as_view(), name="team"),
    path("<int:pk>/view", TeamDetails.as_view(), name="team_view"),
    path("<int:pk>/post/", PostCreateView.as_view(), name="post_create"),

    path('<int:team_pk>/member_manager/<int:member_pk>/',
         views.member_manager,
         name='member_manager'),

    path('<int:team_pk>/request_manager/<int:request_pk>/',
         views.request_manager,
         name='request_manager'),

]
