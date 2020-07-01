from ._base import ListCreateViewSet
from ..serializers import TagSerializer
from ..models import Tag


class ManageTagViewSet(ListCreateViewSet):
    """Manage tags. List and create"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
