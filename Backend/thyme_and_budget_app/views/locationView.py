from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer
from django.contrib.auth import get_user_model


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.get(username=request.data['username'])
        serializer.save(donor=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)