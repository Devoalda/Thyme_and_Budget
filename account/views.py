from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (UserRegistrationSerializer, UserLoginSerializer)


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
                        'user'   : serializer.validated_data}

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {'success'          : True, 'statusCode': status_code, 'message': 'User logged in successfully',
                        'access'           : serializer.data['access'], 'refresh': serializer.data['refresh'],
                        'authenticatedUser': {'username': serializer.validated_data['username'],
                                              'role'    : serializer.validated_data['role']}}

            return Response(response, status=status_code)


from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserListSerializer)


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
                        'user'   : serializer.validated_data}

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {'success'          : True, 'statusCode': status_code, 'message': 'User logged in successfully',
                        'access'           : serializer.data['access'], 'refresh': serializer.data['refresh'],
                        'authenticatedUser': {'username': serializer.validated_data['username'],
                                              'role'    : serializer.validated_data['role']}}

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


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

# class RegisterApi(generics.GenericAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"user"   : UserSerializer(user, context=self.get_serializer_context()).data,
#                              "message": "User Created Successfully. Now perform Login to get your token",
#                              "user_id": user.id, "created_at": timezone.now(), }, status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                     {"errors": serializer.errors, "message": "Registration failed. Please check the provided data.", },
#                     status=status.HTTP_400_BAD_REQUEST)