from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from account.models import Role
from ..models import Collection
from ..serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    throttle_classes = [AnonRateThrottle]

    def _get_collections(self, user):
        if user.is_superuser or user.is_staff:
            return Collection.objects.all()
        elif user.role == Role.DONOR.value:
            return Collection.objects.filter(food_item__donor=user)
        elif user.role == Role.RECEIVER.value:
            return Collection.objects.filter(phone_number=user.phone_number)
        else:
            return Collection.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = request.user.phone_number if request.user.is_authenticated else request.data.get('phone_number')

        try:
            instance = serializer.save(phone_number=phone_number)
        except ValidationError as e:
            # Serialize the error message and return it
            return Response({'Error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    def _apply_filters_and_sorting(self, collections, request):
        # Get the filter parameters from the request
        id_filter = request.query_params.get('id')
        phone_number_filter = request.query_params.get('phone_number')
        quantity_filter = request.query_params.get('quantity')

        # Create Q objects for each filter
        filters = Q()
        if id_filter is not None:
            filters |= Q(id=id_filter)
        if phone_number_filter is not None:
            filters |= Q(phone_number__icontains=phone_number_filter)
        if quantity_filter is not None:
            filters |= Q(quantity=quantity_filter)

        # Apply the filters to the queryset
        collections = collections.filter(filters)

        # Get the sort parameters from the request
        sort_by = request.query_params.get('sort_by')

        # Apply the sorting to the queryset
        if sort_by is not None:
            sort_fields = sort_by.split(',')
            collections = collections.order_by(*sort_fields)

        return collections

    def list(self, request, *args, **kwargs):
        collections = self._get_collections(request.user)
        collections = self._apply_filters_and_sorting(collections, request)
        serializer = self.get_serializer(collections, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        collections = self._get_collections(request.user)
        collections = self._apply_filters_and_sorting(collections, request)

        if self.get_object() not in collections:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied("Only administrators can perform this action.")

        partial = kwargs.pop('partial', True)  # Set partial=True to make the serializer a partial update serializer
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied("Only administrators can perform this action.")
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super(CollectionViewSet, self).get_permissions()
