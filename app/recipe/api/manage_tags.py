from rest_framework import viewsets, permissions, authentication, mixins
from ..serializers import TagSerializer
from ..models import Tag


class ManageTagViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin):
    """Manage tags"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        "filter the queryset with authenticated user."
        return self.queryset.filter(owner=self.request.user)
