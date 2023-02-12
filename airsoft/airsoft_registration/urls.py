import django.urls
from airsoft_registration.views import VoteView
from airsoft_registration.views import TeamRegistrationView, TeamVoteRegistrationView
app_name = "airsoft_registration"
urlpatterns = [


    django.urls.path("vote/<int:pk>", VoteView.as_view(), name="vote"),


        ]