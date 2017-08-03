from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer"""
    url = serializers.HyperlinkedIdentityField(
        view_name='api:category-detail',
        lookup_field='reference_id'
    )
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())
    parent = serializers.HyperlinkedRelatedField(
        view_name='api:category-detail',
        lookup_field='reference_id',
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('url', 'reference_id', 'name', 'parent', 'subcategories',)
