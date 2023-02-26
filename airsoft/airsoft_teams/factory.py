# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import factory
from factory.django import DjangoModelFactory

from airsoft_teams.models import Team


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker('name')
