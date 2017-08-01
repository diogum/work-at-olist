from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Category, Channel


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_id',)
    readonly_fields = ('reference_id',)


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'reference_id', 'channel', 'parent',)
    readonly_fields = ('reference_id',)


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Category, CategoryAdmin)
