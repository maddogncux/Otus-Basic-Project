# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
import random as rand
from random import choices
from string import ascii_letters, digits, ascii_lowercase

from django.contrib.auth.models import AbstractUser
from django.test import Client
from django.test import TestCase

from u_auth.models import UserModel
from .models import TeamMember, Team, TeamRequest


# Create your tests here.

class TestTeamMember(TestCase):

    def setUp(self) -> None:
        self.username = "maddogncux"
        self.password = "".join(choices(ascii_letters + digits, k=10))
        self.user: AbstractUser = UserModel.objects.create_user(
            username=self.username, password=self.password
        )
        team_name = "".join(choices(ascii_lowercase, k=10))
        self.team: Team = Team.objects.create(name=team_name)
        self.team_member: TeamMember = TeamMember.objects.create(team=self.team, user=self.user)
        self.c = Client()

    def test_str(self):
        self.assertEqual(str(self.team_member), 'maddogncux')

    def test_default_role(self):
        self.assertEqual(self.team_member.role, 1)

    def test_set_owner(self):
        self.team_member.set_owner()
        self.assertEqual(self.team_member.role, 4)
        # self.user.has_perm('g_view_team', self.team)
        # self.user.has_perm(('g_create_team_post', self.team))
        # self.user.has_perm('g_team_member_manager', self.team)
        # self.user.has_perm('g_team_vote', self.team)

    def test_set_role(self):
        role = rand.randint(1, 4)
        print('role', role)
        self.team_member.set_role(role=role)
        self.assertEqual(self.team_member.role, role)

    def test_kick(self):
        self.assertIn(self.user, self.team.members.all())
        self.team_member.kick()
        self.assertNotIn(self.user, self.team.members.all())


class TestTeam(TestCase):
    #
    def setUp(self) -> None:
        self.team: Team = Team.objects.create(name="some team name")

    def test_str(self):
        self.assertEqual(str(self.team), "some team name")


class TestTeamRequest(TestCase):
    def setUp(self) -> None:
        username = "maddogncux"
        password = "".join(choices(ascii_letters + digits, k=10))
        self.user: AbstractUser = UserModel.objects.create_user(
            username=username, password=password
        )
        team_name = "".join(choices(ascii_lowercase, k=10))
        self.team: Team = Team.objects.create(name=team_name)
        self.request: TeamRequest = TeamRequest.objects.create(team=self.team, user=self.user)

    def test_str(self):
        self.assertEqual(str(self.request), "maddogncux")

    def test_add_member(self):
        self.assertNotIn(self.user, self.team.members.all())
        self.request.add_member()
        self.assertIn(self.user, self.team.members.all())
        requests = TeamRequest.objects.all()
        self.assertEqual(requests.count(), 0)

    def test_refuse_request(self):
        self.request.refuse_request()
        requests = TeamRequest.objects.all()
        self.assertEqual(requests.count(), 0)

    def test_request_handler_add(self):
        self.assertNotIn(self.user, self.team.members.all())
        self.request.request_handler(key="add")
        self.assertIn(self.user, self.team.members.all())
        requests = TeamRequest.objects.all()
        self.assertEqual(requests.count(), 0)

    def test_request_handler_refuse(self):
        self.request.request_handler(key="refuse")
        requests = TeamRequest.objects.all()
        self.assertEqual(requests.count(), 0)
        self.assertNotIn(self.user, self.team.members.all())
