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
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        self.client.force_authenticate(user=self.user)

        self.location_data = {'postal_code': '569830'}

        # Create a location
        self.location = Location.objects.create(postal_code='138683')

    def test_create_location(self):
        response = self.client.post(reverse('location-list'), self.location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['address'], "180 ANG MO KIO AVENUE 8 NANYANG POLYTECHNIC SINGAPORE 569830")
        self.assertEqual(response.data['location'], "103.848423445403,1.3778190310896")

    def test_read_location(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('location-detail', kwargs={'pk': self.location.pk}), self.location_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_location(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_location(self):
        response = self.client.get(reverse('location-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unauthenticated_user_get_all_location(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('location-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create_location(self):
        self.client.logout()
        response = self.client.post(reverse('location-list'), self.location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_location(self):
        self.client.logout()
        response = self.client.put(reverse('location-detail', kwargs={'pk': self.location.pk}), self.location_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_delete_location(self):
        self.client.logout()
        response = self.client.delete(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_superuser_cannot_delete_location(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('location-detail', kwargs={'pk': self.location.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)