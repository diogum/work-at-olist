from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import Channel


def create_channel(name):
    return Channel.objects.create(name=name)


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
