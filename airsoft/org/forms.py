from django import forms
from .models import Organizations


class OrgForm(forms.ModelForm):
    class Meta:
        model = Organizations
        fields = ["name", "description"]