from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

User = get_user_model()

# Define global variables for username and password
USERNAME = "testuser"
PASSWORD = "testpassword"


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username=USERNAME, password=PASSWORD):
        if username != "" and password != "":
            User.objects.create_user(username=username, password=password)

    def setUp(self):
        # add test data
        self.create_user(USERNAME, PASSWORD)
        self.create_user(USERNAME + "2", PASSWORD + "2")


class UserRegistrationTest(BaseViewTest):

    def test_register_user(self):
        # Test for user registration
        data = {"username": "arbitrary_username", "password": "arbitrary_password",
            "first_name"  : "arbitrary_first_name", "last_name": "arbitrary_last_name",
            "email"       : "arbitrary_email@example.com", "phone_number": "1234567890", "role": "donor", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_existing_username(self):
        # Test for user registration with an existing username
        data = {"username": USERNAME, "password": PASSWORD + "2", "first_name": "test", "last_name": "user",
                "email"   : USERNAME + "@example.com", "phone_number": "1234567890", "role": "donor", }
        self.response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class UserAuthenticationTest(BaseViewTest):

    def test_authenticate_user(self):
        # Test for user authentication
        data = {"username": USERNAME, "password": PASSWORD, "first_name": "test", "last_name": "user",
                "email"   : USERNAME + "@example.com", "phone_number": "1234567890",  # Add other fields here
                }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in self.response.data)
        self.assertTrue("access" in self.response.data)

    def test_authenticate_user_with_invalid_credentials(self):
        # Test for user authentication with invalid credentials
        data = {"username": USERNAME, "password": "wrongpassword", "first_name": "test", "last_name": "user",
                "email"   : USERNAME + "@example.com", "phone_number": "1234567890",  # Add other fields here
                }
        self.response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_is_user_logged_in(self):
        # Test for user login
        self.client.login(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        self.assertTrue(user.is_authenticated)

        # Test for user status
        response = self.client.get(reverse('check_user_login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"is_logged_in": True})

    def test_unauthenticated_user_status(self):
        # Test for unauthenticated user status
        response = self.client.get(reverse('check_user_login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"is_logged_in": False})

class UserLogoutTest(BaseViewTest):

    def test_logout_user(self):
        # Test for user logout
        data = {"username": USERNAME, "password": PASSWORD, "first_name": "test", "last_name": "user",
                "email"   : USERNAME + "@example.com", "phone_number": "1234567890", }
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
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        # Test for updating a user
        self.client.login(username=USERNAME, password=PASSWORD)
        data = {"username": "updateduser", "password": "updatedpassword", "first_name": "test", "last_name": "user",
                "email"   : "test@email2.com", "phone_number": "1234567890", }
        response = self.client.put(reverse('users'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        # Test for deleting a user
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.delete(reverse('users'))  # Changed here
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)