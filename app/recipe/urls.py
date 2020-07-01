from rest_framework import routers
from django.urls import path, include
from .api import ManageTagViewSet, ManageIngredient


app_name = "recipe"


router = routers.DefaultRouter()

router.register("tags", ManageTagViewSet)
router.register('ingredients', ManageIngredient)

urlpatterns = [
    path("", include(router.urls))
]
