from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import FoodItem
from ..serializers import FoodItemSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object or an admin user
        return obj.location.donor == request.user or request.user.is_staff


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer
    parser_classes = [JSONParser]

    def check_permissions(self, request):
        self.get_permissions()
        super(FoodItemViewSet, self).check_permissions(request)

    def get_queryset(self):
        return FoodItem.objects.filter(expiry_date__gt=timezone.now(), quantity__gt=0)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(FoodItemViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.get(id=request.user.id)
        location = user.location_set.first()

        if location is not None:
            serializer.save(location=location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User has no associated location"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request: JSONParser, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_food_items(self, request, *args, **kwargs):
        user_food_items = FoodItem.objects.filter(location__donor=request.user)
        serializer = self.get_serializer(user_food_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)