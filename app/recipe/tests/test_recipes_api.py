from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from ..serializers import RecipeSerializer, RecipeDetailSerializer
from ..models import Ingredient, Tag, Recipe
from django.contrib.auth import get_user_model


def populate_recipe_detail_url(recipe_id):
    "populates the recipe object absolute url"
    return reverse('recipe:recipe-detail', kwargs={"pk": recipe_id})


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
        new_user = get_user_model().objects.create_user(
            email="new@test.com", password="supersecret")
        create_new_recipe(self.user)
        create_new_recipe(new_user)

        res = self.client.get(RECIPE_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = RecipeSerializer(
            Recipe.objects.filter(
                owner=self.user), many=True)

        self.assertEqual(res.data, serializer.data)

    def test_retrieve_one_recipe(self):
        "test retrive a single recipe object detail."
        tag = Tag.objects.create(name="tag1", owner=self.user)

        ingredient = Ingredient.objects.create(
            name="ingredient1", owner=self.user)
        recipe = create_new_recipe(self.user)
        recipe.tags.add(tag)
        recipe.ingredients.add(ingredient)

        url = populate_recipe_detail_url(recipe.id)

        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_new_recipe(self):
        """create recipe without tags and ingredients."""

        payload = {
            "name": "Chocolate cake",
            "cook_minutes": 12,
            "price": 27.50,

        }
        res = self.client.post(RECIPE_LIST, payload,)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(
                payload[key], getattr(recipe, key))

    def create_recipe_with_tags(self):
        """test for creating recipe with tags. uses
        primary key related field"""
        tag = Tag.objects.create(
            name="sample tag",
            owner=self.user)
        tag1 = Tag.objects.create(
            name="sample2 tag", owner=self.user)
        payload = {
            "name": "Chocolate cake",
            "cook_minutes": 12,
            "price": 25,
            "tags": [tag.id, tag1.id],
            "ingredients": []
        }
        res = self.client.post(RECIPE_LIST, payload, "json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe_tags = list(
            Recipe.objects.get(
                id=res.data['id']).tags.all())

        self.assertListEqual(recipe_tags, [tag, tag1])

    def test_create_recipe_with_ingredients(self):
        """test for creating recipe with ingredients. uses
        primary key related field"""
        ingredient = Ingredient.objects.create(
            name="sample tag", owner=self.user)
        ingredient1 = Ingredient.objects.create(
            name="sample2 tag", owner=self.user)
        payload = {
            "name": "Chocolate cake",
            "cook_minutes": 12,
            "price": 25,
            "ingredients": [ingredient.id, ingredient1.id],
            "tags": []
        }
        res = self.client.post(RECIPE_LIST, payload, "json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe_ingredients = list(
            Recipe.objects.get(
                id=res.data['id']).ingredients.all())
        self.assertListEqual(
            recipe_ingredients, [
                ingredient, ingredient1])
