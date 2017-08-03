from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from .models import Category


class CategoryViewSet(viewsets.ViewSet):
    """
    list:
    Return a simple hierarchical tree of all root categories.

    retrieve:
    Return a hierarchical tree of root categories from the given reference_id.

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
