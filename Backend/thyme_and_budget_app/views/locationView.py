from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(donor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)