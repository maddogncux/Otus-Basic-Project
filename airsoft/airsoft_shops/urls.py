from django.urls import path

from .views import ShopListView, ShopCreate, ShopDetails


app_name = "airsoft_shops"
urlpatterns = [
    path("", ShopListView.as_view(), name="shops"),
    path("create/", ShopCreate.as_view(), name="shop_create"),
    path("<int:pk>/", ShopDetails.as_view(), name="shop"),


            ]
