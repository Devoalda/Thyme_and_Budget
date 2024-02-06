from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed database with users and recipes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users and recipes to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        call_command('seed_users', total)
        call_command('seed_recipe', total)