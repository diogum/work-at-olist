from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer"""

    class Meta:
        model = Category
        fields = ('reference_id', 'name',)
