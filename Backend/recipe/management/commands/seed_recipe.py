from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from recipe.models import Recipe


class Command(BaseCommand):
    help = 'Create random recipes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of recipes to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        users = User.objects.all()
        for _ in range(total):
            Recipe.objects.create(author=users[fake.random_int(min=0, max=users.count() - 1)], title=fake.sentence(),
                                  instructions=fake.paragraph(), cooking_time=fake.random_int(min=1, max=300),
                                  budget=fake.random_int(min=1, max=1000), image=fake.image_url())