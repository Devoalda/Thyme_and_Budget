from rest_framework import serializers

from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
        'id', 'title', 'author', 'instructions', 'image_url', 'cooking_time', 'budget', 'created_at', 'updated_at')


# class TodoSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#
#     class Meta:
#         model = Todo
#         fields = ('id', 'title', 'completed', 'user')
