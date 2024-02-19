from rest_framework import serializers

from ..models import Location
from location_service.get_location import GeoOnemap


class LocationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = ['id', 'location', 'address', 'postal_code']

    def validate(self, attrs):
        if 'postal_code' in attrs and attrs['postal_code'] is not None:
            location = GeoOnemap(attrs['postal_code'])
            if location.address is not None and location.longitude is not None and location.latitude is not None:
                attrs['address'] = location.address
                attrs['location'] = location.longitude + ',' + location.latitude
                return attrs
            else:
                raise serializers.ValidationError("Postal code is invalid")
        else:
            raise serializers.ValidationError("Postal code is required")
