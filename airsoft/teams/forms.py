from django import forms
from .models import Teams, MemberRequests


class TeamsForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields = ["name", "city", "Description",]

class MemberForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields = []

class MemberRequestsForm(forms.ModelForm):
    class Meta:
        model = MemberRequests
        fields = []


# class MemberAddForm(forms.ModelForm):
#     class Meta:
#         model = Members
#         fields = []
