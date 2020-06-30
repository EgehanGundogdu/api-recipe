from rest_framework import routers
from django.urls import path, include
from .api import ManageTagViewSet


app_name = "recipe"


router = routers.DefaultRouter()

router.register("tags", ManageTagViewSet)

urlpatterns = [
    path("", include(router.urls))
]
