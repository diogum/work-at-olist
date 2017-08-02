from django.test import TestCase
from django.db.utils import IntegrityError

from ..utils import create_channel, create_category_in_channel


class ChannelTestCase(TestCase):
    """Channel tests."""

    def test__str(self):
        """String representation must be the channel's name."""
        channel = create_channel('String Representation')

        self.assertEqual(str(channel), channel.name)

    def test__name_must_be_unique(self):
        """Channel's name must be unique"""
        create_channel('Unique')

        with self.assertRaises(IntegrityError):
            create_channel('Unique')

    def test__reference_id(self):
        """Reference ID must be the name slugified"""
        channel = create_channel('Channel Name')

        self.assertEqual(channel.reference_id, 'channel-name')


class CategoryTestCase(TestCase):
    """Category tests."""

    def test__str(self):
        """String representation must be the category's name."""
        channel = create_channel('Channel Sample')
        category = create_category_in_channel('String Representation', channel)

        self.assertEqual(str(category), category.name)

    def test__root_category(self):
        """Root category has no parent."""
        channel = create_channel('Channel Sample')
        category = create_category_in_channel('Root Category', channel, parent=None)

        self.assertIsNone(category.parent)
        self.assertTrue(category.is_root_node())

    def test__child_category(self):
        """Child category has parent."""
        channel = create_channel('Channel Sample')
        root = create_category_in_channel('Root Category', channel, parent=None)
        child = create_category_in_channel('Child Category', channel, parent=root)

        self.assertEqual(child.parent, root)
        self.assertTrue(child.is_child_node())

    def test__category_with_children(self):
        """Category can have children."""
        channel = create_channel('Channel Sample')
        root = create_category_in_channel('Root Category', channel, parent=None)
        create_category_in_channel('Child 1 Category', channel, parent=root)
        create_category_in_channel('Child 2 Category', channel, parent=root)

        self.assertEqual(root.get_children().count(), 2)

    def test__category_siblings(self):
        """Category siblings."""
        channel = create_channel('Channel Sample')
        root = create_category_in_channel('Root Category', channel, parent=None)
        child1 = create_category_in_channel('Child 1 Category', channel, parent=root)
        child2 = create_category_in_channel('Child 2 Category', channel, parent=root)

        self.assertEqual(child1.get_next_sibling(), child2)
        self.assertEqual(child2.get_previous_sibling(), child1)

    def test__leaf_category(self):
        """Category is a leaf."""
        channel = create_channel('Channel Sample')
        root = create_category_in_channel('Root Category', channel, parent=None)
        leaf = create_category_in_channel('Leaf Category', channel, parent=root)

        self.assertTrue(leaf.is_leaf_node())

    def test__reference_id_for_root_category(self):
        """For root categories, reference ID must be the channel and category names slugigieds"""
        channel = create_channel('Channel Sample')
        category = create_category_in_channel('Root Category', channel, parent=None)

        self.assertEqual(category.reference_id, 'channel-sample-root-category')

    def test__reference_id_for_child_category(self):
        """For child categories, reference ID must be channel, category parent and category names slugigieds"""
        channel = create_channel('Channel Sample')
        root = create_category_in_channel('Root Category', channel, parent=None)
        child = create_category_in_channel('Child Category', channel, parent=root)

        self.assertEqual(child.reference_id, 'channel-sample-root-category-child-category')

    def test__reference_id_must_be_unique(self):
        """Reference ID must be unique"""
        channel1 = create_channel('First Second')
        create_category_in_channel('Third', channel1, parent=None)
        channel2 = create_channel('First')

        with self.assertRaises(IntegrityError):
            create_category_in_channel('Second Third', channel2, parent=None)
