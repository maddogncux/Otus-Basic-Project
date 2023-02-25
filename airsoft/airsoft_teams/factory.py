from random import choices
from string import ascii_lowercase

from factory.django import DjangoModelFactory
import factory
from airsoft_teams.models import Team


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker('name')
