from django import forms
from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric
from django.contrib.auth.models import User
from .models import UserModel

# Create your forms here.

class UserForm(UserCreationFormGeneric):

	class Meta:
		model = UserModel
		fields = ("username", "email")


