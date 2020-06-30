from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .api import CreateUser
from .serializers import AuthTokenSerializer
app_name = "user"

urlpatterns = [
    path('create/', CreateUser.as_view(), name="create"),
    path(
        'obtain-token/',
        ObtainAuthToken.as_view(serializer_class=AuthTokenSerializer),
        name="obtain-token")
]
