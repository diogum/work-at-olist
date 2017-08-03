from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Channel, Category


class CategoryListSerializer(serializers.ModelSerializer):
    """Category list model serializer"""
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('reference_id', 'name', 'subcategories',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Category detail model serializer"""
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('name', 'reference_id', 'subcategories',)


class ChannelSerializer(serializers.ModelSerializer):
    """Channel model serializer"""

    class Meta:
        model = Channel
        fields = ('reference_id', 'name')
