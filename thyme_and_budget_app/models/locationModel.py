from django.db import models
from location_service.get_location import GeoOnemap


class LocationManager(models.Manager):
    def get_queryset(self):
        return LocationQuerySet(self.model)


class LocationQuerySet(models.QuerySet):
    def get_or_create(self, **kwargs):
        if 'postal_code' in kwargs:
            postal_code = kwargs['postal_code']
            location_record = self.filter(postal_code=postal_code)
            if location_record.exists():
                return location_record.first(), False
            else:
                try:
                    location_object = GeoOnemap(postal_code)
                except Exception as e:
                    raise Exception('Error in LocationQuerySet.get_or_create: ' + str(e))

                return self.create(
                    location=location_object.longitude + ',' + location_object.latitude,
                    address=location_object.address,
                    postal_code=location_object.postal_code
                ), True


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    # donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id', db_column='donor_id',
    #                           db_constraint=True)

    objects = LocationManager()

    def __str__(self):
        return self.address
