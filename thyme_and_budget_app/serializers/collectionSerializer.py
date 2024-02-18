from rest_framework import serializers

from ..models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'phone_number', 'quantity', 'food_item']
        extra_kwargs = {'phone_number': {'required': False}, }