from django.urls import path
from .views import CreateRequest, GroupCreatView, GroupDetailView

app_name = "airsoft_membership"

urlpatterns = [
    # dont need now
    path("<int:pk>/request/", CreateRequest.as_view(), name="create_request"),

    # project path
    path('create/', GroupCreatView.as_view(), name="create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group_detail"),


               ]
