from django.test import TestCase

from .. import serializers
from ..utils import create_channel, create_category_in_channel
from ..models import Channel, Category


class CategoryListSerializerTestCase(TestCase):
    def test__list_items(self):
        """Must be a list of items"""
        channel = create_channel('Channel')
        create_category_in_channel('Category A', channel)
        create_category_in_channel('Category B', channel)
        categories = Category.objects.all()
        serializer = serializers.CategoryListSerializer(instance=categories, context={'request': None}, many=True)

        self.assertIsInstance(serializer.data, list)
        self.assertEqual(len(serializer.data), 2)

    def test__empty_list(self):
        """Test empty category list"""
        categories = Category.objects.all()
        serializer = serializers.CategoryListSerializer(instance=categories, context={'request': None}, many=True)

        self.assertEqual(serializer.data, [])

    def test__contains_expected_fields(self):
        """Item from the list must have the expected fields"""
        channel = create_channel('Channel')
        create_category_in_channel('Category', channel)

        categories = Category.objects.all()
        serializer = serializers.CategoryListSerializer(instance=categories, context={'request': None}, many=True)
        keys = serializer.data[0].keys()

        self.assertEqual(len(keys), 3)
        self.assertIn('reference_id', keys)
        self.assertIn('name', keys)
        self.assertIn('subcategories', keys)


class CategoryDetailSerializerTestCase(TestCase):
    def test__contains_expected_fields(self):
        """Test for expected fields"""
        channel = create_channel('Channel')
        category = create_category_in_channel('Category', channel)
        serializer = serializers.CategoryDetailSerializer(instance=category, context={'request': None})
        keys = serializer.data.keys()

        self.assertEqual(len(keys), 3)
        self.assertIn('reference_id', keys)
        self.assertIn('name', keys)
        self.assertIn('subcategories', keys)


class ChannelSerializerTestCase(TestCase):
    def test__channel_list(self):
        """Must be a list of items"""
        create_channel('Channel A')
        create_channel('Channel B')
        channels = Channel.objects.all()
        serializer = serializers.ChannelSerializer(instance=channels, context={'request': None}, many=True)

        self.assertIsInstance(serializer.data, list)
        self.assertEqual(len(serializer.data), 2)

    def test__empty_list(self):
        """Test empty channel list"""
        channels = Channel.objects.all()
        serializer = serializers.ChannelSerializer(instance=channels, context={'request': None}, many=True)

        self.assertEqual(serializer.data, [])

    def test__contains_expected_fields(self):
        """Test for expected fields"""
        channel = create_channel('Channel')
        serializer = serializers.ChannelSerializer(instance=channel, context={'request': None})
        keys = serializer.data.keys()

        self.assertEqual(len(keys), 2)
        self.assertIn('reference_id', keys)
        self.assertIn('name', keys)
