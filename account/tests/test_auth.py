from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status


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
        data = {"username": "testuser2", "password": "testpassword2", "first_name": "test", "last_name": "user", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_existing_username(self):
        # Test for user registration with an existing username
        data = {"username": "testuser", "password": "testpassword2", "first_name": "test", "last_name": "user", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTest(BaseViewTest):

    def test_authenticate_user(self):
        # Test for user authentication
        data = {"username": "testuser", "password": "testpassword", }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in self.response.data)
        self.assertTrue("access" in self.response.data)

    def test_authenticate_user_with_invalid_credentials(self):
        # Test for user authentication with invalid credentials
        data = {"username": "testuser", "password": "wrongpassword", }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutTest(BaseViewTest):

    def test_logout_user(self):
        # Test for user logout
        data = {"username": "testuser", "password": "testpassword", }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        token = self.response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        self.response = self.client.post(reverse("logout"), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_logout_user_without_token(self):
        # Test for user logout without a token
        self.response = self.client.post(reverse("logout"), format="json")
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)
