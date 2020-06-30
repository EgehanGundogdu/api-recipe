from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Tag
from ..serializers import TagSerializer
TAG_LIST = reverse('recipe:tag-list')


def sample_user(email="test@test.com", password="supersecret"):
    "helper function of creating a sample user."
    return get_user_model().objects.create_user(email, password)


class PublicTagApiTests(TestCase):
    "Public tag list api endpoints tests."

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()

    def test_authentication_required(self):
        "login required for listing tags "
        res = self.client.get(TAG_LIST)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    "Test authorized user tags api."

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.user2 = sample_user(email="user2@test.com")
        self.client.force_authenticate(self.user)

    def test_retrive_all_tags(self):
        "test retrive all tags on db."
        Tag.objects.create(name="Desert", owner=self.user)
        Tag.objects.create(name="Fruit", owner=self.user)

        res = self.client.get(TAG_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = TagSerializer(Tag.objects.all(), many=True)
        self.assertEqual(res.data, serializer.data)

    def test_tag_list_filtered_user(self):
        "test tags were filtered by the user."
        Tag.objects.create(name="Desert", owner=self.user)
        Tag.objects.create(name="Sour", owner=self.user)
        Tag.objects.create(name="Fruit", owner=self.user2)

        res = self.client.get(TAG_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(Tag.objects.all().count(), 3)
