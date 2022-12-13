from django.core import management
from django.core.management.commands import loaddata
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Background worker that picks up and processes DEFEND batches.'

    def handle(self, *args, **options):
        file_names = ['data/fixtures/CatalogueShip.json']
        for file_name in file_names:
            management.call_command('loaddata', file_name)
