from rest_framework import serializers
from .models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    "serializes the tag instances."

    class Meta:
        model = Tag
        fields = [
            "id", "name"
        ]


class IngredientSerializer(serializers.ModelSerializer):
    "serializes the ingredient instances."
    class Meta:
        model = Ingredient
        fields = ["name", "id"]


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = [
            "id"
        ]
