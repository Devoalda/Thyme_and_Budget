from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'phone_number', 'quantity', 'food_item', 'modified_at']
        extra_kwargs = {'phone_number': {'required': False}, }

    def save(self, **kwargs):
        result = super().save(**kwargs)
        if isinstance(result, str):
            raise ValidationError(result)
        return result
