# from django.urls import path
# from . import views
# from .views import (
#     TeamListView,
#     TeamCreateView,
#     TeamDetailView,
#     TeamUpdateView,
#     TeamDeleteView,
#     MemberRequestsView,
#     LeaveTeam,
#     AddMember,
#     KickMember,
#
#     )
# from event.views import Yes, No, Mby,ApplyRegistration
# app_name = "teams"
#
# urlpatterns = [
#     # Team links
#
#     path("", TeamListView.as_view(), name="teams"),
#     path('create/', TeamCreateView.as_view(), name="create"),
#     path('<slug:slug>/', TeamDetailView.as_view(), name="team"),
#     path('<slug:slug>/confirm-delete/', TeamDeleteView.as_view(), name="delete"),
#     path('<slug:slug>/edit', TeamUpdateView.as_view(), name="edit"),
#
#     # Teams members links
#     path('<slug:slug>/leave/', LeaveTeam.as_view(), name="leave_team"),
#     path('<slug:slug>/<int:pk>/kick/', KickMember.as_view(), name="kick"),
#     path('<slug:slug>/member_request', MemberRequestsView.as_view(), name="member-request"),
#     path('<slug:slug>/<int:pk>/Apply/',  ApplyRegistration.as_view(), name="Apply"),
#     path('<slug:slug>/<int:pk>/yes/', Yes.as_view(), name="yes"),
#     path('<slug:slug>/<int:pk>/no/', No.as_view(), name="no"),
#     path('<slug:slug>/<int:pk>/mby/', Mby.as_view(), name="mby"),
#     path('<slug:slug>/edit/', TeamUpdateView.as_view(), name="edit"),
#     path('<slug:slug>/<int:pk>/add/', AddMember.as_view(), name="add"),
#
# ]
