import os
import tempfile
from PIL import Image
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

    def test_partial_update_recipe(self):
        """test for partial update recipe objects."""
        recipe = create_new_recipe(
            self.user,
            name="Chicken wings", price=12.00, cook_minutes=12)
        ingredient = Ingredient.objects.create(
            name="meanless ingredient", owner=self.user
        )
        url = populate_recipe_detail_url(recipe.id)

        payload = {
            "name": "Updated wings!",
            "ingredients": [ingredient.id]
        }
        res = self.client.patch(url, payload, "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])

    def test_full_update_recipe(self):
        """test fully update recipe uses put method."""
        recipe = create_new_recipe(
            self.user,
            name="Chicken wings", price=12.00, cook_minutes=12)
        url = populate_recipe_detail_url(recipe.id)
        tag = Tag.objects.create(
            name="meanless tag",
            owner=self.user)
        payload = {
            "name": "Updated wings",
            "price": 481.32,
            "cook_minutes": 15,
            "tags": [tag.id],
            "ingredients": []
        }
        res = self.client.put(url, payload, "json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.tags.all().count(), 1)
        self.assertEqual(recipe.name, payload['name'])


def recie_image_upload_url(recipe):
    "populate the recipe image upload url."
    return reverse('recipe:recipe-upload-image',
                   kwargs={"pk": recipe.id})


class RecipeImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="supersecret")

        self.recipe = create_new_recipe(self.user)
        # force authenticate user.
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_recipe_image_upload(self):
        "test to recipe image upload with temp file."
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new('RGB', (100, 100))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            url = recie_image_upload_url(self.recipe)
            payload = {"image": ntf}
            res = self.client.post(url, payload, format="multipart")
        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_invalid_image_payload(self):
        "test invalid image "
        payload = {"image": "bad bad"}
        url = recie_image_upload_url(self.recipe)
        res = self.client.post(url, payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
