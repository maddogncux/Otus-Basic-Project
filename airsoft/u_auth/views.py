from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import UserForm


# Create your views here.


class MeView(TemplateView):
    template_name = "u_auth/me.html"


class LoginView(LoginViewGeneric):
    next_page = reverse_lazy('homepage:index')


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy('homepage:index')


# must be a viewFunction
class UserCreateView(CreateView):
    form_class = UserForm
    template_name = 'registration/register.html'
    context_object_name = "User"
    success_url = reverse_lazy('homepage:index')
