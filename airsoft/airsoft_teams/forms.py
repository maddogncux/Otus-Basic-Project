from airsoft_teams.models import TeamPost
from django import forms


class TeamPostForm(forms.ModelForm):
    # template_name = "team_post_create.html"
    class Meta:

        model = TeamPost
        fields = ["body",]


