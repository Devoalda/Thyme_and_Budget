from django.core.validators import validate_image_file_extension
from django.http import QueryDict
from rest_framework import serializers

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, validators=[validate_image_file_extension])
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Recipe
        fields = ['title', 'author', 'instructions', 'image', 'cooking_time', 'budget', 'created_at', 'updated_at']
        extra_kwargs = {'author': {'required': False}}  # Make 'author' optional

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            data = data.dict()
        return super().to_internal_value(data)