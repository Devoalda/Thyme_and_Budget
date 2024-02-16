from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import FoodItem, Location

User = get_user_model()


class CollectionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.location = Location.objects.create(postal_code='12345', donor=self.user)

        self.collection_data = {'phone_number': '1234567890', 'quantity': 100000, 'food_item': 1}

        # Create a food item with id 1
        self.food_item = FoodItem.objects.create(id=1, name='1234', expiry_date='2024-02-16', quantity=100000,
                                                 location=self.location)
        # Create a collection
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.collection_id = response.data['id']  # Save the id of the created collection

    def test_create_collection_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_collection_authenticated(self):
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_collection(self):
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)