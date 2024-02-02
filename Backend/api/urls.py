from django.urls import path, include
# from .views import TodoList, TodoDetail
from .views import RecipeList, RecipeDetail

urlpatterns = [
    # path('recipes/', RecipeList.as_view(), name='recipe_list'),
    # path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe_detail'),
]
