from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'role', 'Phone_number')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        email=validated_data['email']
                                        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'Phone_number')
        extra_kwargs = {'password': {'write_only': True}, }