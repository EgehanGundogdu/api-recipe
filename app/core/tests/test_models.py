from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test1@gmail.com", password="super secret"
        )

    def test_create_user_with_email(self):
        """Test creating a new user with email instead of username"""
        user = get_user_model().objects.create_user(
            email="test@test.com", password="super_secret"
        )
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("super_secret"))

    def test_create_user_with_invalid_email(self):
        """
        Test creating user with invalid email. Raises an error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="", password="super secret")

    def test_create_new_super_user(self):
        """
        Test create a super user.
        """
        user = get_user_model().objects.create_superuser(
            email="super@user.com", password="123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
