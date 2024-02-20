from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, AuthUser

from .models import User, Role


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=128, write_only=True)
    last_name = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=128, write_only=True)
    role = serializers.ChoiceField(choices=[(role.value, role.name) for role in Role], write_only=True)
    phone_number = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'role', 'phone_number')

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise PermissionDenied({"username": "A user with this username already exists."})

        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise PermissionDenied({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)

        return {'username'    : auth_user.username, 'first_name': auth_user.first_name,
                'last_name'   : auth_user.last_name, 'email': auth_user.email, 'role': auth_user.role,
                'phone_number': auth_user.phone_number, 'created_date': auth_user.created_date, }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {'access': access_token, 'refresh': refresh_token, 'username': user.username,
                          'role'  : user.role, 'id': user.id}

            return validation
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'email', 'phone_number', 'role', 'date_joined', 'created_date', 'modified_date')
        read_only_fields = ('date_joined', 'created_date', 'modified_date')

    def validate(self, data):
        # Check if 'role' or 'username' is in the data
        if 'role' in data or 'username' in data:
            raise serializers.ValidationError("Updating 'role' and 'username' is not allowed.")
        return data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)