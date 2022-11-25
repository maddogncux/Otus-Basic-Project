from django import forms
from .models import BasicGroup


class BasicGroupForms(forms.ModelForm):
    name = forms.CharField(label='name', max_length=64)
    city = forms.CharField(label='city', max_length=64)

    class Meta:
        model = BasicGroup
        fields = ["name", "city", ]
        exclude = ["is_private", "owner"]
