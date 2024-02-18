from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Collection
from ..serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            try:
                user = get_user_model().objects.get(id=request.user.id)
                if user.phone_number:
                    serializer.save(phone_number=user.phone_number, quantity=request.data['quantity'])
                else:
                    raise AttributeError
            except AttributeError:
                try:
                    if request.data['phone_number']:
                        serializer.save(phone_number=request.data['phone_number'], quantity=request.data['quantity'])
                except KeyError:
                    return Response({"error": "User has no associated phone number"},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)