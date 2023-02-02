from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric

from .models import UserModel


# Create your forms here.

class UserForm(UserCreationFormGeneric):
    class Meta:
        model = UserModel
        fields = ("username", "email")
