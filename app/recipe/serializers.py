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
        fields = [
            "id",
            "name",
            "tags",
            "ingredients",
            "cook_minutes",
            "price"]
        read_only_fields = [
            "id"
        ]
        # extra_kwargs = {
        #     "tags": {
        #         "allow_blank": True,
        #     },
        #     "ingredients": {
        #         "allow_blank": True
        #     }
        # }


class RecipeDetailSerializer(RecipeSerializer):
    """serializes the single recipe object. inherit from recipe serializer"""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):
        ...
