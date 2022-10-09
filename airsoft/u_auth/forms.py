from django import forms
from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric
from django.contrib.auth.models import User
from .models import UserModel

# Create your forms here.

class UserForm(UserCreationFormGeneric):

	class Meta:
		model = UserModel
		fields = ("username", "email")


		# def __init__(self, *args, **kwargs):
		# 	super().__init__(*args, **kwargs)
		#
		# 	for name, field in self.fields.items():
		# 		# print(name, field, field.widget)
		# 		widget: Widget = field.widget
		# 		widget.attrs["class"] = "form-control"







	#
	# def save(self, commit=True):
	# 	user = super(UserForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user