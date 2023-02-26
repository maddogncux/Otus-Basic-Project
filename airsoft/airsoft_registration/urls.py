# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import django.urls

from airsoft_registration.views import VoteView

app_name = "airsoft_registration"
urlpatterns = [

    django.urls.path("vote/<int:pk>", VoteView.as_view(), name="vote"),

]
