# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric

from .models import UserModel


# Create your forms here.

class UserForm(UserCreationFormGeneric):
    class Meta:
        model = UserModel
        fields = ("username", "email")
