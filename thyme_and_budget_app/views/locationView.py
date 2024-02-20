from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer
from django.contrib.auth import get_user_model


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = get_user_model().objects.get(username=request.data['username'])
        record = self.queryset.filter(postal_code=request.data['postal_code'])
        if record.exists():
            return Response(record.values(), status=status.HTTP_200_OK)
        # serializer.save(donor=user)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)