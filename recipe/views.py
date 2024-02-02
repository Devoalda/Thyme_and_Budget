from django.http import QueryDict
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.content_type == 'multipart/form-data':
            image = request.FILES['image']
            data = QueryDict(mutable=True)
            data.update(request.POST)
            data['author'] = request.user.id  # retrieve author from request user
            recipe = Recipe.objects.create(image=image, **data)
            return Response({'status': 'success', 'data': RecipeSerializer(recipe).data},
                            status=status.HTTP_201_CREATED)
        elif request.content_type == 'application/json':
            return super().create(request, *args, **kwargs)
