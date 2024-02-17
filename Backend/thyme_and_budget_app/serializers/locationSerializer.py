from rest_framework import serializers

from ..models import Location


class LocationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = ['id', 'location', 'address', 'postal_code']