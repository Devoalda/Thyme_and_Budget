import random

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

        # List of possible titles
        titles = ["Spaghetti Carbonara", "Chicken Parmesan", "Beef Stroganoff", "Vegetable Stir Fry", "Fish Tacos",
                  # Add more titles as needed
                  ]

        # List of possible instructions
        instructions = ["Boil water. Add pasta. Cook for 10 minutes. Drain.",
                        "Season chicken with salt and pepper. Cook in pan for 15 minutes. Serve with rice.",
                        "Mix beef with onions and mushrooms. Cook for 20 minutes. Serve with mashed potatoes.",
                        "Stir fry vegetables in pan with soy sauce. Serve with rice.",
                        "Grill fish. Serve in tortillas with salsa and guacamole.",  # Add more instructions as needed
                        ]

        for _ in range(total):
            Recipe.objects.create(author=users[fake.random_int(min=0, max=users.count() - 1)],
                                  title=random.choice(titles), instructions=random.choice(instructions),
                                  cooking_time=fake.random_int(min=1, max=300), budget=fake.random_int(min=1, max=1000),
                                  image=f"https://picsum.photos/200/300?random={fake.random_int(min=1, max=1000)}&food")