import base64
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from recipe.models import Recipe
from rest_framework import status
from rest_framework.test import APIClient


class RecipeViewSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.image_path = os.path.join(settings.BASE_DIR, 'recipe/tests/test_image.jpg')
        cls.recipe_name = 'Test_Recipe'
        with open(cls.image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Construct image data in the format "data:image/jpeg;base64,<base64-encoded-data>;filename=<filename>"
            image_data = f"data:image/jpeg;base64,{image_data};filename={cls.recipe_name}.jpg"

        cls.recipe_data = {"title" : "Test Recipe", "instructions": "Test Instructions", "cooking_time": 30,
                           "budget": "100", "image": image_data}

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.response = self.client.post(reverse_lazy('recipe-list'), data=self.recipe_data, format='json')

    def tearDown(self):
        recipe = Recipe.objects.first()
        if recipe and recipe.image:
            # print(f"Deleting image at {os.path.join(settings.MEDIA_ROOT, recipe.image.path)}")
            os.remove(os.path.join(settings.MEDIA_ROOT, recipe.image.path))

    def test_create_recipe(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertQuerysetEqual(Recipe.objects.all(), ['Test Recipe'], transform=str)

    def test_get_recipe(self):
        recipe = Recipe.objects.get()
        response = self.client.get(reverse_lazy('recipe-detail', kwargs={'pk': recipe.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Recipe')

    def test_update_recipe(self):
        recipe = Recipe.objects.get()
        self.recipe_name = 'Updated_Recipe'
        with open(self.image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Construct image data in the format "data:image/jpeg;base64,<base64-encoded-data>;filename=<filename>"
            image_data = f"data:image/jpeg;base64,{image_data};filename={self.recipe_name}.jpg"

        new_data = {"title" : "Updated Recipe", "instructions": "Updated Instructions", "cooking_time": 45,
                    "budget": 150, "image": image_data}

        response = self.client.put(reverse_lazy('recipe-detail', kwargs={'pk': recipe.id}), data=new_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get().title, 'Updated Recipe')

    def test_delete_recipe(self):
        recipe = Recipe.objects.get()
        response = self.client.delete(reverse_lazy('recipe-detail', kwargs={'pk': recipe.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerysetEqual(Recipe.objects.all(), [])