import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker
from thyme_and_budget_app.models.foodModel import FoodItem
from thyme_and_budget_app.models.locationModel import Location  # replace with the actual path to your models


class Command(BaseCommand):
    help = 'Create random food items'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of food items to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        for _ in range(total):
            # Get a random location or create a new one if none exist
            location = Location.objects.order_by('?').first()
            if not location:
                location = Location.objects.create(location=fake.city(), address=fake.address(),
                                                   postal_code=fake.random_int(min=10000, max=99999)
                                                   # generates a random 5-digit number
                                                   )
            # Generate a random image
            image_url = f"https://source.unsplash.com/random?food,{fake.word(ext_word_list=['pizza', 'burger', 'salad', 'sushi', 'steak'])}"
            response = requests.get(image_url)
            image_name = image_url.split("/")[-1]  # Use the last part of the URL as the image name

            food_item = FoodItem(name=fake.catch_phrase(),
                                 expiry_date=fake.date_between(start_date='+1d', end_date='+1y'),
                                 # generates a random date between tomorrow and one year from now
                                 quantity=fake.random_int(min=1, max=100),
                                 # generates a random integer between 1 and 100
                                 location=location)
            food_item.image.save(f"{image_name}.jpg",  # Save the image with the name we got earlier
                                 ContentFile(response.content))  # Save the image to the 'image' field
            food_item.save()