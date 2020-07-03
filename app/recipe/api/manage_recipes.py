from rest_framework import viewsets, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Recipe
from ..serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    RecipeImageSerializer)


class ManageRecipe(viewsets.ModelViewSet):
    "manage recipe objects. all methods supported."
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        "filter the queryset with authenticated user."
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        "assocaite a foreign key with user"
        serializer.save(owner=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        """Returns the serializer class according to the action type."""
        if self.action == "retrieve":
            "this means request to object detail."
            return RecipeDetailSerializer
        elif self.action == "upload_image":
            return RecipeImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path="image-upload")
    def upload_image(self, request, *args, **kwargs):
        "handle recipe image uploads."
        recipe = self.get_object()
        serializer = self.get_serializer(
            instance=recipe, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors,
                        status.HTTP_400_BAD_REQUEST)
