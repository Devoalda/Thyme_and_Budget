import base64

from django.core.files.base import ContentFile
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            data = request.data.copy()
            image_data = data.pop('image', None)

            if image_data:
                try:
                    image_file = self.extract_image_from_data(image_data)
                    data['image'] = image_file
                except ValueError as e:
                    return self.invalid_image_response(str(e))

            serializer = self.get_and_validate_serializer(data)
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return self.unsupported_media_type_response()

    def extract_image_from_data(self, image_data):
        delimiter = ';base64,'
        filename_delimiter = ';filename='

        parts = image_data.split(delimiter)
        # metadata = parts[0]
        base64_data = parts[1]

        filename_parts = base64_data.split(filename_delimiter)
        image_name = filename_parts[1].strip('"')

        return ContentFile(base64.b64decode(base64_data), name=image_name)

    def invalid_image_response(self, error_message):
        return Response({'error': f'Invalid image data: {error_message}'}, status=status.HTTP_400_BAD_REQUEST)

    def get_and_validate_serializer(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def unsupported_media_type_response(self):
        return Response({'error': 'Unsupported content type. Only JSON requests are accepted.'},
                        status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)