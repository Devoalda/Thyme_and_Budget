import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import FoodItem, Location

User = get_user_model()


class FoodTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.location = Location.objects.create(postal_code='12345', donor_id=cls.user.id)
        with open('thyme_and_budget_app/tests/test_image.jpg', 'rb') as image_file:
            cls.image = base64.b64encode(image_file.read())  # remove the decode('utf-8') call here
            data = ContentFile(cls.image, name='temp.jpg')  # create a Django ContentFile
        cls.food_data = {'name': '1234', 'expiry_date': '2024-02-16', 'quantity': 100000, 'image': data, }

        cls.food_item = FoodItem.objects.create(name='1234', expiry_date='2024-02-16', quantity=100000, image=data,
                                                location=cls.location)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_read_food(self):
        response = self.client.get(reverse('food-detail', kwargs={'pk': self.food_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_update_food(self):
        # Convert the ContentFile object back to a base64 string
        image_data = base64.b64encode(self.food_data['image'].read()).decode('utf-8')
        # Update the 'image' field in the food_data dictionary
        self.food_data['image'] = image_data
        response = self.client.put(reverse('food-detail', kwargs={'pk': self.food_item.pk}), self.food_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_delete_food(self):
        response = self.client.delete(reverse('food-detail', kwargs={'pk': self.food_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_user_cannot_read_food(self):
        self.client.logout()
        response = self.client.get(reverse('food-detail', kwargs={'pk': self.food_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_food(self):
        self.client.logout()
        response = self.client.put(reverse('food-detail', kwargs={'pk': self.food_item.pk}), self.food_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_read_food(self):
        self.client.logout()
        response = self.client.get(reverse('food-detail', kwargs={'pk': self.food_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_update_non_existent_food(self):
        response = self.client.put(reverse('food-detail', kwargs={'pk': 999}), self.food_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_non_existent_food(self):
        response = self.client.delete(reverse('food-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)