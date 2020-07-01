from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Ingredient
from django.contrib.auth import get_user_model
from ..serializers import IngredientSerializer

INGREDIENT_LIST = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):
    "test of public endpoints for ingredients api."

    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_retrive_lists(self):
        "test login required to retrive ingredients list."
        res = self.client.get(INGREDIENT_LIST)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    "test of private endpoints for ingredients api."

    def setUp(self):
        "setup api client. create test users and forced to authenticate."
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="supersecret")
        self.user2 = get_user_model().objects.create_user(
            email="user2@test.com", password="supersecret"
        )
        Ingredient.objects.create(name="Cucumber", owner=self.user)
        Ingredient.objects.create(name="Tomato", owner=self.user)
        Ingredient.objects.create(name="Pepper", owner=self.user2)
        self.client.force_authenticate(self.user)

    def test_retrive_all_ingredients(self):
        "test retrieve owned ingredients."

        res = self.client.get(INGREDIENT_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.filter(owner=self.user)
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_new_ingredient(self):
        "test create new ingreient"
        payload = {"name": "Black Pepper"}
        res = self.client.post(INGREDIENT_LIST, payload, "json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Ingredient.objects.filter(
                name="Black Pepper").exists())

    def test_create_new_ingredient_invalid_payload(self):
        "test of post the wrong payload"
        invalid_payload = {"name": ""}
        res = self.client.post(
            INGREDIENT_LIST, invalid_payload, "json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
