from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import PermissionDenied, ValidationError

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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        collections = self._get_collections(request.user)
        if self.get_object() not in collections:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        collections = self._get_collections(request.user)
        serializer = self.get_serializer(collections, many=True)
        return Response(serializer.data)

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