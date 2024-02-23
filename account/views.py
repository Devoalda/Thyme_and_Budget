from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserListSerializer)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {'success': True, 'statusCode': status_code, 'message': 'User logged in successfully',
                        'access': serializer.data['access'], 'refresh': serializer.data['refresh'],
                        'authenticatedUser': {'username': serializer.validated_data['username'],
                                              'role': serializer.validated_data['role']}}

            return Response(response, status=status_code)


class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid()

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {'success': True, 'statusCode': status_code, 'message': 'User successfully registered!',
                        'user': serializer.validated_data}

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {'success': True, 'statusCode': status_code, 'message': 'User logged in successfully',
                        'access': serializer.data['access'], 'refresh': serializer.data['refresh'],
                        'authenticatedUser': {'username': serializer.validated_data['username'],
                                              'role': serializer.validated_data['role']}}

            return Response(response, status=status_code)


class UserRetrieveUpdateDestroyView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckUserStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserListSerializer(request.user)
            return JsonResponse({
                "is_logged_in": True,
                "username": request.user.username,
                "role": serializer.data['role'],
            })
        else:
            return JsonResponse({"is_logged_in": False})


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
