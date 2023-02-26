from django.contrib.auth.models import Permission
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,

)

from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import UserForm
from .models import UserModel

# Create your views here.


class MeView(TemplateView):
    template_name = "u_auth/me.html"


class LoginView(LoginViewGeneric):
    next_page = reverse_lazy('homepage:index')


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy('homepage:index')


# must be a viewFunction
class UserCreateView(CreateView):
    model = UserModel
    form_class = UserForm
    template_name = 'registration/register.html'
    context_object_name = "User"
    success_url = reverse_lazy('homepage:index')

    def form_valid(self, form):
        return super().form_valid(form)

class UserEditProfile(UpdateView):
    pass






# def register_request(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect("homepage:index")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = NewUserForm()
#     return render(request=request,
#     template_name="registration/register.html",
#     context={"register_form": form})
