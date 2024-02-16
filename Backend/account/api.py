from django.contrib.auth import logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"request.data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user"   : UserSerializer(user, context=self.get_serializer_context()).data,
                         "message": "User Created Successfully.  Now perform Login to get your token", }, status=201)


class UserApi(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # Logout a user
        logout(request)
        return Response(status=status.HTTP_200_OK)