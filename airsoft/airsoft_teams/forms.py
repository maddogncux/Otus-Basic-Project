# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from django import forms

from airsoft_teams.models import TeamPost


class TeamPostForm(forms.ModelForm):
    # template_name = "team_post_create.html"
    class Meta:
        model = TeamPost
        fields = ["body", ]
