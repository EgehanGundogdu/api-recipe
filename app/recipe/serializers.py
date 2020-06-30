from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    "serializes the tag instances."

    class Meta:
        model = Tag
        fields = [
            "id", "name"
        ]
