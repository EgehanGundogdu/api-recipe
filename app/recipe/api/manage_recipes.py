from rest_framework import viewsets, authentication, permissions
from ..models import Recipe
from ..serializers import RecipeSerializer, RecipeDetailSerializer


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
        return self.serializer_class
