from django.db import models
from .locationModel import Location


class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name