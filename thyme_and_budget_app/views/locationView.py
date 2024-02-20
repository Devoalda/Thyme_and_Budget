from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer
from django.contrib.auth import get_user_model


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['create', 'retrieve', 'update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = self.queryset.filter(postal_code=request.data['postal_code'])
        if record.exists():
            return Response(record.values(), status=status.HTTP_200_OK)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)