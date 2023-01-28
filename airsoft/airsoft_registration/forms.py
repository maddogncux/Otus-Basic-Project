from django.shortcuts import get_object_or_404

from airsoft_teams.models import Team, Members
from .models import TeamRegistration
from django import forms


class TeamRegForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TeamRegForm, self).__init__(*args, **kwargs)
        member = get_object_or_404(Members, user=self.request.user, main=True)
        print(str(member))
        team = Team.objects.get(pk=member.team.id)
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
