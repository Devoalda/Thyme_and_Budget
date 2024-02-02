from rest_framework import generics
# from .serializers import TodoSerializer
# from todo.models import Todo

from .serializers import RecipeSerializer
from recipe.models import Recipe


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

# class TodoList(generics.ListCreateAPIView):
#     permission_classes = (IsOwnerOnly,)  # added
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     # added
#     def filter_queryset(self, queryset):
#         queryset = queryset.filter(user=self.request.user)
#         return super().filter_queryset(queryset)


# class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsOwnerOnly,)  # added
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
