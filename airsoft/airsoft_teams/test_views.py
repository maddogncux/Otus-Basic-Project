from django.core.exceptions import PermissionDenied
from django.test import Client
from random import choices
from string import ascii_letters, digits, ascii_lowercase
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from guardian.shortcuts import assign_perm

from .models import Team_Member, Team, TeamRequest
from u_auth.models import UserModel

class TestTeamListView(TestCase):
    def setUp(self) -> None:

        self.team_name = "".join(choices(ascii_lowercase, k=12))
        self.team: Team = Team.objects.create(name=self.team_name)
        self.c = Client()

    def tearDown(self) -> None:
        print('test end')


    def test_response_sc(self):
        response = self.client.get("/teams/")
        self.assertEqual(response.status_code, 200, u'need perm')

    def test_context(self):
        response = self.client.get("/teams/")
        self.assertIn(self.team_name, str(response.context))

class TestTeamDetails(TestCase):

    def setUp(self) -> None:
        team_name = "".join(choices(ascii_lowercase, k=12))
        self.team: Team = Team.objects.create(name=team_name)
        self.c = Client()

    def tearDown(self) -> None:
        print('test end')
    def test_response_sc(self):
        response = self.client.get(f'/teams/{self.team.pk}/view', {}, True)
        self.assertEqual(response.status_code, 200, u'its ok ')





class TestTeamMemberDetails(TestCase):

    def setUp(self) -> None:
        self.username = "".join(choices(ascii_lowercase, k=10))
        self.password = "".join(choices(ascii_letters + digits, k=10))
        self.user: AbstractUser = UserModel.objects.create_user(
            username=self.username, password=self.password
        )
        team_name = "".join(choices(ascii_lowercase, k=12))
        self.team: Team = Team.objects.create(name=team_name)
        self.c = Client()

    def tearDown(self) -> None:
        print('test end')

    def test_user_no_perm_view(self):
        self.c.login(username=self.user.username, password=self.password)
        response = self.c.get(f'/teams/{self.team.pk}', {}, True)
        self.assertEqual(response.status_code, 403, u'need perm')


    def test_user_have_perm_view(self):
        assign_perm('g_view_team', self.user, self.team)
        self.c.login(username=self.user.username, password=self.password)
        response = self.c.get(f'/teams/{self.team.pk}', {}, True)
        self.assertEqual(response.status_code, 200, u'can view')



