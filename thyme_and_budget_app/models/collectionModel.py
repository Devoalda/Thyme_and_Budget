from django.db import models

from .foodModel import FoodItem


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number