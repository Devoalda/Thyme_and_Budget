from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
from thyme_and_budget_app.models.locationModel import Location

User = get_user_model()


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        for _ in range(total):
            role = fake.random_element(elements=('donor', 'receiver'))
            user = User.objects.create_user(username=fake.unique.user_name(), email=fake.email(), password='123456',
                    first_name=fake.first_name(), last_name=fake.last_name(), phone_number=fake.phone_number(),
                    role=role)
            if role == 'donor':
                Location.objects.create(location=fake.city(), address=fake.address(),
                        postal_code=fake.random_int(min=10000, max=99999))  # generates a random 5-digit number
                        # donor=user)