from django.urls import path
from .views import CreateRequest

app_name = "airsoft_membership"

urlpatterns = [
    path("<int:pk>/request/", CreateRequest.as_view(), name="create_request"),



               ]
