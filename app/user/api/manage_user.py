from rest_framework import generics
from rest_framework import permissions
from rest_framework import authentication
from ..serializers import UserSerializer


class ManageUser(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Return authenticated user."""
        return self.request.user
