# pylint: disable=invalid-name

from http import HTTPStatus
from random import choices
from string import ascii_lowercase, ascii_letters, digits

from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from u_auth.models import UserModel


# Create your tests here.
class LoginTestCase(TestCase):
    url = reverse_lazy("u_auth:login")
    url1 = reverse_lazy("u_auth:register")

    def setUp(self) -> None:
        # TeamFactory.create()
        username = "".join(choices(ascii_lowercase, k=10))
        password = "".join(choices(ascii_letters + digits, k=10))
        user: AbstractUser = UserModel.objects.create_user(
            username=username, password=password
        )
        self.user = user
        self.password = password

    def tearDown(self) -> None:
        """not needed """
        print('test end')

    def test_login(self):
        response_a = self.client.post(
            self.url,
            {
                "username": self.user.username,
                "password": self.password,
            }
        )
        self.assertEqual(response_a.url, reverse('homepage:index'))
        response_f = self.client.get(response_a.url)
        self.assertFalse(response_f.context["user"].is_anonymous)


class RegistrationTestCase(TestCase):
    url = reverse_lazy("u_auth:register")

    def setUp(self) -> None:
        users = UserModel.objects.all()
        self.user_before = users.count()
        username = "".join(choices(ascii_lowercase, k=10))
        password = "".join(choices(ascii_letters + digits, k=10))
        user: AbstractUser = UserModel.objects.create_user(
            username=username, password=password
        )
        self.user = user
        self.password = password
        print(users.count())

    def tearDown(self) -> None:
        print('test end')

    def test_Registration(self):
        response = self.client.post(
            self.url,
            {
                "username": self.user.username,
                "password1": self.password,
                "password2": self.password,
                "email": "test@mail.ru"

            }
        )

        users = UserModel.objects.all()
        self.assertEqual(users.count(), int(self.user_before) + 1)
        self.client.login(username=self.user.username, password=self.password)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["user"].is_anonymous)
