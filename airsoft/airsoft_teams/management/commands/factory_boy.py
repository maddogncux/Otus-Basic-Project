from django.core.management.base import BaseCommand
from airsoft_teams.factory import TeamFactory


class Command(BaseCommand):
    help = 'fill bd with teams'

    def handle(self, *args, **options):
        print('Make Teams')

        TeamFactory.create()
