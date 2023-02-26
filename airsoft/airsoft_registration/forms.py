# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from django import forms

from airsoft_teams.models import Team
from .models import TeamRegistration


class TeamRegForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        team = self.request.user.team_profile.team
        # member = get_object_or_404(Members, user=self.request.user, main=True)
        print(str(team))
        team = Team.objects.get(pk=team.id)
        print(str(team))
        users = team.members.all()
        for user in users:
            print(str(user))
        self.fields['user'].queryset = users

    class Meta:
        model = TeamRegistration
        fields = ["side", ]

    user = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
