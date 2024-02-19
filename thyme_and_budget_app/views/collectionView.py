from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Collection
from ..serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = []

    def _check_authentication(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        return None

    def _check_admin(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only administrators can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return None

    def _check_donor(self, request):
        if not get_user_model().objects.get(id=request.user.id).role == 'donor':
            return Response({"error": "Only donors can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return None

    def _handle_validation_errors(self, serializer, phone_number, quantity):
        try:
            serializer.save(phone_number=phone_number, quantity=quantity)
        except ValidationError as e:
            return Response({"error": str(e).strip('[]').strip('\'')}, status=status.HTTP_400_BAD_REQUEST)
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid data. Please check your input and try again."},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            user = get_user_model().objects.get(id=request.user.id)
            phone_number = user.phone_number
        elif 'phone_number' in request.data:
            phone_number = request.data['phone_number']
        else:
            return Response({"error": "Phone number is required for unauthenticated users."},
                            status=status.HTTP_400_BAD_REQUEST)

        validation_response = self._handle_validation_errors(serializer, phone_number, request.data['quantity'])
        if validation_response:
            return validation_response

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        admin_response = self._check_admin(request)
        if admin_response:
            return admin_response
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        admin_response = self._check_admin(request)
        if admin_response:
            return admin_response
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        donor_response = self._check_donor(request)
        if donor_response:
            return donor_response
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def collections_by_phone(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        phone_number = get_user_model().objects.get(id=request.user.id).phone_number
        collections = Collection.objects.filter(phone_number=phone_number)
        serializer = self.get_serializer(collections, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
