from rest_framework import viewsets, authentication, permissions
from ..models import Recipe
from ..serializers import RecipeSerializer


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
