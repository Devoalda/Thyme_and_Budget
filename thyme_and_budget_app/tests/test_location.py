from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from ..models import Location

User = get_user_model()


class LocationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.location_data = {'postal_code': '12345', 'username': 'testuser'}

        # Create a location
        self.location = Location.objects.create(postal_code='12345', donor=self.user)

    def test_create_location(self):
        response = self.client.post(reverse('location-list'), self.location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_location(self):
        response = self.client.get(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        response = self.client.put(reverse('location-detail', kwargs={'pk': self.location.pk}), self.location_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_location(self):
        response = self.client.delete(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)