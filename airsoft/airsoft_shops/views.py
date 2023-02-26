# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import ListView, CreateView, DetailView

from airsoft_shops.models import Shop, Member

# Create your views here.


UserModel: AbstractUser = get_user_model()


class ShopCreate(CreateView):
    template_name = "shop_create.html"
    context_object_name = "shop"
    # success_url =
    model = Shop
    # form_class =
    fields = ["name", "city", "description", "logo", "address", "gps"]

    def form_valid(self, form):
        user = self.request.user
        # user_in_team = Team.objects.filter(members=user)
        # if len(user_in_team) == 1:
        #     return HttpResponseRedirect("/teams/create/")
        # else:
        #     # go = None  # optio
        obj = form.save(commit=False)
        obj.save()
        obj.members.add(user)
        form.save_m2m()
        change_role = get_object_or_404(Member, user=user, team=obj)
        Member.set_owner(change_role)
        return HttpResponseRedirect(f"/shops/{obj.id}")


class ShopListView(ListView):
    context_object_name = "shops"
    template_name = "shops.html"
    queryset = (Shop
                .objects
                # .select_related()
                # .prefetch_related()
                .all())


class ShopDetails(DetailView):
    template_name = 'shop.html'
    context_object_name = "shop"
    model = Shop

    # Move to user manger  (mby use in include templates?)
    def post(self, request, *args, **kwargs, ):
        if request.method == 'POST':
            shop = get_object_or_404(Shop, pk=self.kwargs["pk"])
            shop.request_handler(request=request, user=self.request.user)
            return HttpResponseRedirect(f"/shops/{shop.id}")
