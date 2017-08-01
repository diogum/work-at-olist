from tempfile import NamedTemporaryFile
from unittest.mock import patch
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError


class ImportcategoriesCommandTestCase(TestCase):
    def test__required_arguments(self):
        """Test for required arguments"""
        with self.assertRaises(CommandError) as cm:
            call_command('importcategories')
        self.assertEqual(cm.exception.args[0],
                         'Error: the following arguments are required: channel_name, csv_filename')

    def test__file_not_exists_exception(self):
        """An exception must be raised if the file is not found"""
        with self.assertRaises(CommandError) as cm:
            call_command('importcategories', 'channel name', 'wrong file')
        self.assertEqual(cm.exception.args[0], "Error: wrong file not found")

    @patch('channels.utils.import_categories')
    def test__call_action(self, mock):
        """Test if command is calling the action with the right arguments"""
        with NamedTemporaryFile(mode='r', encoding='utf-8') as f:
            call_command('importcategories', 'channel name', f.name)
        mock.assert_called_once_with('channel name', [])
