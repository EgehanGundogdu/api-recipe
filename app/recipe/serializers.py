from rest_framework import serializers
from .models import Tag, Ingredient


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
