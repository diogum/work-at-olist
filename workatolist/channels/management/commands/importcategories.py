import os

from django.core.management.base import BaseCommand, CommandError

from channels.utils import import_categories


class Command(BaseCommand):
    """Command to import categories to a channel"""
    help = 'Import categories from a CSV file to a channel'

    def add_arguments(self, parser):
        parser.add_argument('channel_name', type=str, help='Channel name to import categories')
        parser.add_argument('csv_filename', type=str, help='CSV filename with categories')

    def handle(self, *args, **options):
        if not os.path.exists(options['csv_filename']):
            raise CommandError("Error: {} not found".format(options['csv_filename']))

        with open(options['csv_filename'], 'r', encoding='utf-8') as f:
            categories = [item.strip() for item in f]

        import_categories(options['channel_name'], categories[1:])
