from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from .models import Channel, Category


class CategoryViewSet(viewsets.ViewSet):
    """
    list:
    Returns a simple hierarchical tree of all root categories.

    retrieve:
    Returns a hierarchical tree of root categories from the given reference_id.

    """
    lookup_field = 'reference_id'
    lookup_url_kwarg = 'reference_id'

    def list(self, request):
        queryset = Category.objects.root_nodes()
        serializer = serializers.CategoryListSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, reference_id=None):
        queryset = Category.objects.all()
        categories = get_object_or_404(queryset, reference_id=reference_id)
        serializer = serializers.CategoryDetailSerializer(categories, context={'request': request})
        return Response(serializer.data)


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a simple list of channel.

    retrieve:
    Returns details of the given channel.

    """
    lookup_field = 'reference_id'
    lookup_url_kwarg = 'reference_id'
    queryset = Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
