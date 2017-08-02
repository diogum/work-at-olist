from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from ..models import Channel, Category
from ..utils import import_categories, create_channel, create_category_in_channel


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


class CreateChannelTestCase(TestCase):
    def test__create_channel(self):
        """Must create the channel"""
        expected_channel = create_channel('Created Channel')
        channel = Channel.objects.get(name='Created Channel')

        self.assertEqual(expected_channel.id, channel.id)


class CreateCategoryTestCase(TestCase):
    def test__create_category_in_channel(self):
        """Must create the category in the given channel with the specified name"""
        channel = Channel.objects.create(name='Created Channel')
        expected_category = create_category_in_channel('Created Category', channel)
        category = channel.categories.get(name='Created Category')

        self.assertEqual(expected_category.id, category.id)

    def test__create_category_with_parent(self):
        """The category must have parent"""
        channel = Channel.objects.create(name='Created Channel')
        parent_category = create_category_in_channel('Parent Category', channel, parent=None)
        create_category_in_channel('Child Category', channel, parent=parent_category)
        child_category = Category.objects.get(name='Child Category')

        self.assertIsNotNone(child_category.parent)
