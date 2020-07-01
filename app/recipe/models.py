from django.db import models
from django.conf import settings
# Create your models here.


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

    def __str__(self):
        "string representation of recipe objects."
        return self.name
