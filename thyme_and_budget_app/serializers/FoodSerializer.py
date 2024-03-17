import requests
from django.core.files.base import ContentFile
from django.core.validators import validate_image_file_extension
from django.http import QueryDict
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .locationSerializer import LocationSerializer
from ..models import FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
            max_length=None, use_url=True,
    )

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'expiry_date', 'quantity', 'image', 'created_at', 'updated_at', 'location', 'donor']

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            data = data.dict()
        return super().to_internal_value(data)

    def validate_image(self, value):
        if isinstance(value, str) and value.startswith('http'):
            response = requests.get(value)
            image_name = value.split("/")[-1]
            value = ContentFile(response.content, name=image_name)
        return value

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary representation, adding the image and location details.
        """
        # Get the default representation
        representation = super().to_representation(instance)

        # Add the image to the representation if it exists and is a URL
        if instance.image and str(instance.image).startswith('http'):
            representation['image'] = str(instance.image)

        if instance.location:
            # Prefer the address if it exists, otherwise use the postal code
            if instance.location.address != "":
                representation['location'] = instance.location.address
            else:
                representation['location'] = instance.location.postal_code

        return representation
