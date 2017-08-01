from django.contrib import admin

from .models import Category, Channel


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_id', 'channel', 'parent',)


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Category, CategoryAdmin)
