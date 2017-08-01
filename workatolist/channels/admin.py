from django.contrib import admin

from .models import Category, Channel

admin.site.register(Channel)
admin.site.register(Category)
