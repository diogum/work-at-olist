from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class BaseModel(models.Model):
    """Abstract base class that provides primary key, reference id, creation and modification timestamp."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reference_id = models.SlugField(_('Reference ID'), max_length=255, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        abstract = True

    def generate_reference_id(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.reference_id = self.generate_reference_id()
        super(BaseModel, self).save(*args, **kwargs)


class Channel(BaseModel):
    """Channels model for marketplaces."""

    name = models.CharField(_('Name'), max_length=30, unique=True)

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        return self.name

    def generate_reference_id(self):
        return slugify(self.name)


class Category(MPTTModel, BaseModel):
    """Hierarchical model for categories."""

    name = models.CharField(_('Name'), max_length=30)
    channel = models.ForeignKey(Channel, related_name='categories', verbose_name=_('Channel'))
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def generate_reference_id(self):
        if self.parent:
            reference_fields = [self.channel.name, self.parent, self.name]
        else:
            reference_fields = [self.channel.name, self.name]

        return '-'.join(map(slugify, reference_fields))
