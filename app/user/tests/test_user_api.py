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
ME_URL = reverse('user:me')


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

    def test_fail_to_retrive_user_unauthorized(self):
        """
        test retrive user with unauthorized user.
        """

        res = self.client.get(ME_URL)

        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Tests for public user app endpoints.
    Such as retrive,update and delete user info.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**{
            "email": "test@test.com", "password": "supersecret"
        })
        self.client.force_authenticate(self.user)

    def test_retrive_user_page(self):
        """test retrive user own page."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('email', res.data)
        self.assertNotIn('password', res.data)

    def test_update_own_info_partial(self):
        """
        test update owned user info partial..
        """
        payload = {"email": "updated@test.com"}
        res = self.client.patch(ME_URL, payload, "json")
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])

    def test_method_not_allowed(self):
        """
        test rejected to post method on user me url.
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_info_fully(self):
        """
        test update owned user info completely.
        """
        payload = {
            "email": "updated@test.com", "password": "updated_super_secret"
        }
        res = self.client.put(ME_URL, payload, "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.email, payload['email'])

    def test_fail_existing_email(self):
        """
        test updating user profile with already registered email.
        """
        payload = {
            "email": "existing@test.com",
            "password": "existing"}
        create_user(**payload)

        update_payload = {"email": "existing@test.com"}

        res = self.client.patch(ME_URL, update_payload, "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_owned_account(self):
        """
        test delete owned account successfully.
        """
        res = self.client.delete(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.all().count(), 0)
