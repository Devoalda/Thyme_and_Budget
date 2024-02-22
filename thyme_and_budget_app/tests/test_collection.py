from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import FoodItem, Location
from account.models import Role

User = get_user_model()


class CollectionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.collector = User.objects.create_user(username='testuser', password='testpassword', role=Role.RECEIVER.value,
                                             phone_number='1234567890')

        self.donor = User.objects.create_user(username='donor', password='donorpassword', role=Role.DONOR.value,
                                             phone_number='1234')

        self.superuser = User.objects.create_superuser(username='superuser',
                                                       password='superpassword')  # Create a superuser
        self.client.force_authenticate(user=self.collector)
        self.location = Location.objects.create(postal_code='12345')

        self.collection_data = {'phone_number': '1234567890', 'quantity': 100, 'food_item': 1}

        # Create a food item with id 1
        self.food_item = FoodItem.objects.create(id=1, name='1234', expiry_date='2024-02-16', quantity=100000,
                                                 location=self.location, donor=self.donor)
        # Create a collection
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.collection_id = response.data['id']  # Save the id of the created collection

    def test_update_collection_updated_at(self):
        self.client.force_authenticate(user=self.superuser)  # Authenticate as superuser

        # Get the collection before the update
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))
        updated_at_before = response.data['modified_at']

        # Send the PUT request
        collection_data = {}
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.collection_id}), collection_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the collection after the update
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))
        updated_at_after = response.data['modified_at']

        # Check if the updated_at field has been updated
        self.assertNotEqual(updated_at_before, updated_at_after)

    def test_update_collection_others(self):
        self.client.force_authenticate(user=self.superuser)  # Authenticate as superuser

        # Define the new values for the fields
        new_phone_number = '0987654321'
        new_quantity = 200
        new_food_item = 1

        # Send the PUT request with the new values
        collection_data = {'phone_number': new_phone_number, 'quantity': new_quantity, 'food_item': new_food_item}
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.collection_id}), collection_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the updated collection
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))

        # Check if the fields have been updated
        self.assertEqual(response.data['phone_number'], new_phone_number)
        self.assertEqual(response.data['quantity'], new_quantity)
        self.assertEqual(response.data['food_item'], new_food_item)

    def test_update_collection_unauthenticated(self):
        self.client.logout()
        collection_data = {}
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.collection_id}), collection_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collection_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_collection_authenticated(self):
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_collection(self):
        self.client.force_authenticate(user=self.superuser)  # Only donors can read collections
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_create_collection_as_collector(self):
        self.client.force_authenticate(user=self.collector)  # Authenticate as collector

        # Send the POST request with the collection data
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json')

        # Check if the collection was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_collection_as_donor(self):
        self.client.force_authenticate(user=self.donor)  # Authenticate as donor

        # Send the GET request for the collection of a food item that the donor has donated
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.collection_id}))

        # Check if the collection was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)