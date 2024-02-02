from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe


class RecipeViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.recipe_data = {'title': 'Test Recipe', 'instructions': 'Test Instructions', 'cooking_time': 30,
                            'image': 'http://testimage.com', 'budget': 100, }
        self.response = self.client.post(reverse('recipe-list'), self.recipe_data, format='json')

    def test_create_recipe(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Test Recipe')

    def test_get_recipe(self):
        recipe = Recipe.objects.get()
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': recipe.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Recipe')

    def test_update_recipe(self):
        recipe = Recipe.objects.get()
        new_data = {'title' : 'Updated Recipe', 'instructions': 'Updated Instructions', 'cooking_time': 45,
                    'budget': 150, }
        response = self.client.put(reverse('recipe-detail', kwargs={'pk': recipe.id}), new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get().title, 'Updated Recipe')

    def test_delete_recipe(self):
        recipe = Recipe.objects.get()
        response = self.client.delete(reverse('recipe-detail', kwargs={'pk': recipe.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)