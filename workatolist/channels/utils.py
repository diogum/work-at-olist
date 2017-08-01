from django.db import transaction
from .models import Category, Channel


@transaction.atomic
def import_categories(channel_name, categories):
    """
    Import categories into a specified channel.

    :param channel_name: The channel where the categories will be imported.
                         The channel will be created if it not exists.
    :param categories: A list of categories hierarchy separated by '/', e.g., "['Root / Child A / Child B']".

    """
    channel, created = Channel.objects.get_or_create(name=channel_name)

    if not created:
        channel.categories.all().delete()

    for item in categories:
        parent = None
        for category in item.split('/'):
            parent, _ = Category.objects.get_or_create(channel=channel, name=category.strip(), parent=parent)
