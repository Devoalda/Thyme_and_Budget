import base64

from django.core.files.base import ContentFile
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrAdmin]
        return super(RecipeViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        image_data = data.pop('image', None)

        if image_data:
            image_file = self.extract_image_from_data(image_data)
            data['image'] = image_file

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def extract_image_from_data(self, image_data: str)-> ContentFile:
        """
        Extracts the image from the data and returns a ContentFile object
        """
        delimiter = ';base64,'
        filename_delimiter = ';filename='

        parts = image_data.split(delimiter)
        base64_data = parts[1]

        filename_parts = base64_data.split(filename_delimiter)
        image_name = filename_parts[1].strip('"')

        return ContentFile(base64.b64decode(filename_parts[0]), name=image_name)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        image_data = data.pop('image', None)

        if image_data:
            image_file = self.extract_image_from_data(image_data)
            data['image'] = image_file

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request: JSONParser, *args, **kwargs) -> Response:
        """
        Handle partial update of the recipe
        """
        data = request.data.copy()
        image_data = data.pop('image', None)

        if image_data:
            image_file = self.extract_image_from_data(image_data)
            data['image'] = image_file

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)