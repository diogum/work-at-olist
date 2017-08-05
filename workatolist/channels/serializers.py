from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Channel, Category


class CategoryListSerializer(serializers.ModelSerializer):
    """Category list model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:categories-detail',
        lookup_field='reference_id'
    )
    channel = serializers.HyperlinkedRelatedField(
        view_name='api:channels-detail',
        lookup_field='reference_id',
        read_only=True
    )
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('name', 'url', 'reference_id', 'channel', 'subcategories',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Category detail model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:categories-detail',
        lookup_field='reference_id'
    )
    parent = serializers.HyperlinkedRelatedField(
        view_name='api:categories-detail',
        lookup_field='reference_id',
        read_only=True
    )
    channel = serializers.HyperlinkedRelatedField(
        view_name='api:channels-detail',
        lookup_field='reference_id',
        read_only=True
    )
    subcategories = serializers.ListSerializer(source='children', child=RecursiveField())

    class Meta:
        model = Category
        fields = ('name', 'url', 'reference_id', 'channel', 'parent', 'subcategories',)


class ChannelListSerializer(serializers.ModelSerializer):
    """Channel list model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:channels-detail',
        lookup_field='reference_id'
    )

    class Meta:
        model = Channel
        fields = ('name', 'url', 'reference_id',)


class ChannelDetailSerializer(serializers.ModelSerializer):
    """Channel detail model serializer"""

    url = serializers.HyperlinkedIdentityField(
        view_name='api:channels-detail',
        lookup_field='reference_id'
    )
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        root_categories = obj.categories.filter(parent=None)
        serializer = CategoryListSerializer(root_categories, context={'request': self.context['request']}, many=True)
        return serializer.data

    class Meta:
        model = Channel
        fields = ('name', 'url', 'reference_id', 'categories',)
