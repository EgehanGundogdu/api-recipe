from django.db import models
from django.conf import settings
import os
import uuid
# Create your models here.


def generate_recipe_image_path(instance, filename):
    "generates dynamic file upload path with uuid."
    file_extension = filename.split('.')[-1]
    generated_name = f"{uuid.uuid4()}.{file_extension}"
    return os.path.join('uploads/recipe/', generated_name)


class Tag(models.Model):
    """Tag model."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_tags')
    name = models.CharField(max_length=30)

    def __str__(self):
        "String representation of tag instance."
        return self.name


class Ingredient(models.Model):
    "Ingredient model."
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def __str__(self):
        "String representation of ingredient instance"
        return self.name


class Recipe(models.Model):
    "recipe objects."
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    cook_minutes = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    tags = models.ManyToManyField('recipe.Tag')
    ingredients = models.ManyToManyField('recipe.Ingredient')
    link = models.URLField(blank=True)
    image = models.ImageField(blank=True,
                              upload_to=generate_recipe_image_path)

    def __str__(self):
        "string representation of recipe objects."
        return self.name
