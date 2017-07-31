from uuid import uuid4
from django.db import models


class BaseModel(models.Model):
    """Abstract base class that provides primary key, creation and modification timestamp."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Channel(BaseModel):
    """Channels model for marketplaces."""

    name = models.CharField('Name', max_length=30, unique=True)

    def __str__(self):
        return self.name
