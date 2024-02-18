from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'food', FoodItemViewSet, basename='food')
router.register(r'location', LocationViewSet, basename='location')
router.register(r'collection', CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]
