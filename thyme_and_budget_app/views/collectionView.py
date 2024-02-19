from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
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
        if not request.user.is_donor:
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

        auth_response = self._check_authentication(request)
        if auth_response:
            return auth_response

        user = get_user_model().objects.get(id=request.user.id)
        if user.phone_number:
            validation_response = self._handle_validation_errors(serializer, user.phone_number,
                                                                 request.data['quantity'])
            if validation_response:
                return validation_response
        elif 'phone_number' in request.data:
            validation_response = self._handle_validation_errors(serializer, request.data['phone_number'],
                                                                 request.data['quantity'])
            if validation_response:
                return validation_response
        else:
            return Response({"error": "User has no associated phone number."}, status=status.HTTP_400_BAD_REQUEST)

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