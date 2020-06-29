from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class CoreAppAdminTests(TestCase):
    """
    Custom user model admin actions test.
    """

    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@hey.com", password=123
        )

        self.client.force_login(self.admin)

        self.user = get_user_model().objects.create_user(
            email="normal@normal.com", password=123
        )

    def test_created_user_in_admin_list(self):
        """
        Viewing the django administration panel user list
        """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test user edit page works.
        """
        url = reverse('admin:core_user_change', args=(self.user.id,))
        res = self.client.get(url)
        self.assertEqual(
            res.status_code, 200
        )

    def test_new_user_create_page(self):
        """
        Test new user create page works
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
