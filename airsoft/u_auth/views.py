from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric



)
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect

# Create your views here.

class MeView(TemplateView):
    template_name = "u_auth/me.html"


class LoginView(LoginViewGeneric):
    next_page = reverse_lazy('homepage:index')

class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy('homepage:index')



# must be a view
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			# login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})