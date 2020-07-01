from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from ..serializers import RecipeSerializer
from ..models import Ingredient, Tag, Recipe
from django.contrib.auth import get_user_model


def create_new_recipe(user, **kwargs):
    "helper function creating a new recipe"
    default = {
        "name": "Recipe sample",
        "cook_minutes": 12,
        "price": 12.00
    }
    if kwargs:
        default.update(kwargs)
    return Recipe.objects.create(
        owner=user, **default
    )


RECIPE_LIST = reverse('recipe:recipe-list')


class PublicApiTests(TestCase):
    "Test public api endpoints."

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        "test login required to access public api"
        res = self.client.get(RECIPE_LIST)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            **{"email": "test@test.com", "password": "supersecret"}
        )
        self.client.force_authenticate(self.user)

    def test_retrive_user_recipes(self):
        """
        test get owned recipes.
        """
        tag = Tag.objects.create(name="tag1", owner=self.user)
        tag1 = Tag.objects.create(name="tag2", owner=self.user)
        ingredient = Ingredient.objects.create(
            name="ingredient1", owner=self.user)
        ingredient2 = Ingredient.objects.create(
            name="ingredient2", owner=self.user)
        create_new_recipe(
            self.user,)
        # tags=[
        #     tag, tag1],
        # ingredients=[
        #     ingredient, ingredient2])
        res = self.client.get(RECIPE_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = RecipeSerializer(Recipe.objects.all(), many=True)
        self.assertEqual(res.data, serializer.data)
