from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from ..models import Channel
from ..utils import import_categories


class ImportcategoriesTestCase(TestCase):
    def test__channel_is_created_if_not_exists(self):
        """The channel must be created if it not exists"""
        with self.assertRaises(ObjectDoesNotExist):
            Channel.objects.get(name='New channel')

        import_categories('New channel', [])
        channel = Channel.objects.get(name='New channel')

        self.assertEqual(channel.name, 'New channel')

    def test__empty_categories(self):
        """Categories should be excluded if an empty list is passed as a parameter"""
        import_categories('Channel', ['Category'])
        channel = Channel.objects.get(name='Channel')

        self.assertEqual(len(channel.categories.all()), 1)

        import_categories('Channel', [])
        channel = Channel.objects.get(name='Channel')

        self.assertEqual(len(channel.categories.all()), 0)

    def test__import_categories_hierarchy(self):
        """Test for imported categories"""
        categories_to_import = [
            'Root',
            'Root / Child A',
            'Root / Child A / Child B',
        ]
        import_categories('Channel', categories=categories_to_import)
        channel = Channel.objects.get(name='Channel')
        categories = channel.categories.all()

        self.assertEqual(len(categories), 3)
        self.assertTrue(categories[0].is_root_node)
        self.assertTrue(categories[1].is_child_node)
        self.assertTrue(categories[2].is_leaf_node)
