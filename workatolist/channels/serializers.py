from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer"""
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('reference_id', 'name', 'subcategories',)
