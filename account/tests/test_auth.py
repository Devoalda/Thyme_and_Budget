from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

User = get_user_model()


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username="", password=""):
        if username != "" and password != "":
            User.objects.create_user(username=username, password=password)

    def setUp(self):
        # add test data
        self.create_user("testuser", "testpassword")


class UserRegistrationTest(BaseViewTest):

    def test_register_user(self):
        # Test for user registration
        data = {"username": "testuser2", "password": "testpassword2", "first_name": "test", "last_name": "user",
            "email"       : "testuser2@example.com", "phone_number": "1234567890", "role": "donor", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_existing_username(self):
        # Test for user registration with an existing username
        data = {"username": "testuser", "password": "testpassword2", "first_name": "test", "last_name": "user",
            "email"       : "testuser@example.com", "phone_number": "1234567890", "role": "donor", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class UserAuthenticationTest(BaseViewTest):

    def test_authenticate_user(self):
        # Test for user authentication
        data = {"username": "testuser", "password": "testpassword", "first_name": "test", "last_name": "user",
            "email"       : "testuser@example.com", "phone_number": "1234567890", # Add other fields here
        }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in self.response.data)
        self.assertTrue("access" in self.response.data)

    def test_authenticate_user_with_invalid_credentials(self):
        # Test for user authentication with invalid credentials
        data = {"username": "testuser", "password": "wrongpassword", "first_name": "test", "last_name": "user",
            "email"       : "testuser@example.com", "phone_number": "1234567890", # Add other fields here
        }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutTest(BaseViewTest):

    def test_logout_user(self):
        # Test for user logout
        data = {"username": "testuser", "password": "testpassword", "first_name": "test", "last_name": "user",
            "email"       : "testuser@example.com", "phone_number": "1234567890", }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        token = self.response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        self.response = self.client.post(reverse("logout"), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_logout_user_without_token(self):
        # Test for user logout without a token
        self.response = self.client.post(reverse("logout"), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRetrieveUpdateDestroyViewTest(BaseViewTest):

    def test_retrieve_user(self):
        # Test for retrieving a user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users'))  # Changed here
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        # Test for updating a user
        self.client.login(username='testuser', password='testpassword')
        data = {"username": "updateduser", # Add other fields here
        }
        response = self.client.put(reverse('users'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        # Test for deleting a user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(reverse('users'))  # Changed here
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)