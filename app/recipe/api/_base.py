from rest_framework import (
    viewsets,
    mixins,
    permissions,
    authentication)


class ListCreateViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    base viewset for listing and creating endpoints
    uses token authentication.
    and accepts authenticated user requests.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        "filter the queryset with authenticated user"
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        "association instance with the authenticated user"
        serializer.save(owner=self.request.user)
