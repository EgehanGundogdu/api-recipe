from ._base import ListCreateViewSet
from ..models import Ingredient
from ..serializers import IngredientSerializer


class ManageIngredient(ListCreateViewSet):
    "manage the ingredient objects."
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
