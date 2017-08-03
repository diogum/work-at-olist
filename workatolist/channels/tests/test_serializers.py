from django.test import TestCase

from ..serializers import CategorySerializer
from ..utils import create_channel, create_category_in_channel
from ..models import Category


class CategorySerializerTestCase(TestCase):
    def test__category_list(self):
        """Must be a list of items"""
        channel = create_channel('Channel')
        create_category_in_channel('Category A', channel)
        create_category_in_channel('Category B', channel)
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)

        self.assertIsInstance(serializer.data, list)
        self.assertEqual(len(serializer.data), 2)

    def test__empty_list(self):
        """Test empty category list"""
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)

        self.assertEqual(serializer.data, [])

    def test__contains_expected_fields(self):
        """Test for expected fields"""
        channel = create_channel('Channel')
        category = create_category_in_channel('Category', channel)
        serializer = CategorySerializer(instance=category)
        keys = serializer.data.keys()

        self.assertEqual(len(keys), 3)
        self.assertIn('reference_id', keys)
        self.assertIn('name', keys)
        self.assertIn('subcategories', keys)
