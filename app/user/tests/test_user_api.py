from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


def create_user(**params):
    """New user-creating auxiliary function."""
    return get_user_model().objects.create_user(
        **params
    )


CREATE_USER_URL = reverse('user:create')
OBTAIN_TOKEN_URL = reverse('user:obtain-token')


class PublicUserApiTests(TestCase):
    """
    Tests for public user app endpoints. Such as create new user.
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_new_user(self):
        """
        User creation endpoint test with valid credentials.
        """
        payload = {
            "email": "test@test.com",
            "password": "superpass",
            "first_name": "test",
            "last_name": "test"
        }
        res = self.client.post(
            CREATE_USER_URL, payload, format="json")
        self.assertEqual(
            res.status_code, status.HTTP_201_CREATED
        )

        user = get_user_model().objects.get(email="test@test.com")
        self.assertEqual(
            user.email, payload.get('email')
        )
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_with_short_password(self):
        """
        Test create new user with short password.
        """
        payload = {
            "email": "test@test.com",
            "password": "123",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_user_existing_email(self):
        """Test creating a user that already exists fail."""
        payload = {
            "email": "test@test.com",
            "password": "supersecret"}
        create_user(**payload)
        res = self.client.post(
            CREATE_USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(get_user_model().objects.all().count(), 1)

    def test_fail_create_user_with_numeric_passw(self):
        """
        Test creating a user with fully numeric password.
        """
        payload = {
            "email": "test@test.com",
            "password": 123
        }

        res = self.client.post(CREATE_USER_URL, payload, "json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token(self):
        """
        test of the user's token successfully returned.
        """
        payload = {
            "email": "test@test.com", "password": "supersecret"}
        create_user(**payload)
        res = self.client.post(
            OBTAIN_TOKEN_URL, payload, "json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_fail_obtain_token_with_wrong_password(self):
        """
        test of fail obtain token with wrong password.
        """
        payload = {
            "email": "test@test.com",
            "password": "supersecret"}
        create_user(**payload)
        res = self.client.post(
            OBTAIN_TOKEN_URL, {
                "email": "test@test.com", "password": "wrong_pass"})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_fail_obtain_token_with_no_registered_user(self):
        """
        test of fail making token request with the unregistered user.
        """
        payload = {"email": "wrong@test.com", "password": "wrong"}
        res = self.client.post(OBTAIN_TOKEN_URL, payload, "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
