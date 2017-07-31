# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
