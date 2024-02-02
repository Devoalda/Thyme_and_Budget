from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutritionValueViewSet

router = DefaultRouter()
router.register(r'', NutritionValueViewSet, basename='nutritionValue')

urlpatterns = [
    path('', include(router.urls)),
]