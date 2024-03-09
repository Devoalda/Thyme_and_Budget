from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Role
from ..models import FoodItem, Location
from ..serializers import FoodItemSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object or an admin user
        # return obj.location.donor == request.user or request.user.is_staff
        return obj.donor == request.user or request.user.is_staff


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer
    parser_classes = [JSONParser]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the filter parameters from the request
        id_filter = request.query_params.get('id')
        name_filter = request.query_params.get('name')
        date_filter = request.query_params.get('expiry_date')
        donor_filter = request.query_params.get('donor')
        location_filter = request.query_params.get('location')

        # Create Q objects for each filter
        filters = Q()
        if id_filter is not None:
            filters |= Q(id=id_filter)
        if name_filter is not None:
            filters |= Q(name__icontains=name_filter)
        if date_filter is not None:
            filters |= Q(expiry_date=date_filter)
        if donor_filter is not None:
            filters |= Q(donor__username__icontains=donor_filter)
        if location_filter is not None:     # Not tested
            filters |= Q(location__postal_code__icontains=location_filter)

        # Apply the filters to the queryset
        queryset = queryset.filter(filters)

        # Get the sort parameters from the request
        sort_by = request.query_params.get('sort_by')

        # Apply the sorting to the queryset
        if sort_by is not None:
            sort_fields = sort_by.split(',')
            queryset = queryset.order_by(*sort_fields)

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def check_permissions(self, request):
        self.get_permissions()
        super(FoodItemViewSet, self).check_permissions(request)

    def get_queryset(self):
        return FoodItem.objects.filter(expiry_date__gt=timezone.now(), quantity__gt=0)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            if self.request.user.is_authenticated and self.request.user.role == Role.RECEIVER:
                raise PermissionDenied("Receivers are not allowed to create a food item.")
            else:
                self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(FoodItemViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['donor'] = user.id

        # Extract the postal_code from the request data
        postal_code = request.data.get('postal_code')

        # check if the postal_code is in the request data and if it is not empty and it is 6 digits
        if postal_code is None or postal_code == "" or len(postal_code) != 6:
            return Response({"Collection Postal Code": ["This field is required and must be 6 digits long."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a Location with the same postal_code already exists
        try:
            location, created = Location.objects.get_or_create(postal_code=postal_code)
        except Exception as e:
            return Response({"Collection Postal Code": ["Cannot find the address with provided postal code, please "
                                                        "check again."]}, status=status.HTTP_400_BAD_REQUEST)

        # Use the existing or new Location for the FoodItem
        request.data['location'] = location.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = request.user
        request.data['donor'] = user.id

        # Extract the postal_code from the request data
        postal_code = request.data.get('postal_code')

        # check if the postal_code is in the request data and if it is not empty and it is 6 digits
        if postal_code is None or postal_code == "" or len(postal_code) != 6:
            return Response({"Collection Postal Code": ["This field is required and must be 6 digits long."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a Location with the same postal_code already exists
        try:
            location, created = Location.objects.get_or_create(postal_code=postal_code)
        except Exception as e:
            return Response({"Collection Postal Code": ["Cannot find the address with provided postal code, please "
                                                        "check again."]}, status=status.HTTP_400_BAD_REQUEST)

        # Use the existing or new Location for the FoodItem
        request.data['location'] = location.id

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request: JSONParser, *args, **kwargs) -> Response:
        user = request.user
        request.data['donor'] = user.id

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_food_items(self, request, *args, **kwargs):
        user_food_items = FoodItem.objects.filter(donor_id=request.user.id)
        serializer = self.get_serializer(user_food_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
