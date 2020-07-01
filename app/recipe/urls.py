from rest_framework import routers
from django.urls import path, include
from .api import ManageTagViewSet, ManageIngredient, ManageRecipe


app_name = "recipe"


router = routers.DefaultRouter()

router.register("tags", ManageTagViewSet)
router.register('ingredients', ManageIngredient)
router.register('recipes', ManageRecipe)

urlpatterns = [
    path("", include(router.urls))
]
