from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Channel, Category


class CategoryListSerializer(serializers.ModelSerializer):
    """Category list model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:categories-detail',
        lookup_field='reference_id'
    )
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('name', 'url', 'reference_id', 'subcategories',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Category detail model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:categories-detail',
        lookup_field='reference_id'
    )
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('name', 'url', 'reference_id', 'subcategories',)


class ChannelSerializer(serializers.ModelSerializer):
    """Channel model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:channel-detail',
        lookup_field='reference_id'
    )

    class Meta:
        model = Channel
        fields = ('name', 'url', 'reference_id',)
