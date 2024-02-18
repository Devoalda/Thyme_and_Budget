from django.contrib.auth import logout
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AuthUser

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


class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {'success': False, 'status_code': status.HTTP_403_FORBIDDEN,
                        'message': 'You are not authorized to perform this action'}
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = AuthUser.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {'success': True, 'status_code': status.HTTP_200_OK, 'message': 'Successfully fetched users',
                        'users'  : serializer.data

                        }
            return Response(response, status=status.HTTP_200_OK)


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