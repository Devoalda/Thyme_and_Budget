from django.conf import settings
from django.db import models


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id', db_column='donor_id',
                              db_constraint=True)

    def __str__(self):
        return self.address