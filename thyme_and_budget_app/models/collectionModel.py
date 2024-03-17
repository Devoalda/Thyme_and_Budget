from django.db import models, transaction
from rest_framework.exceptions import ValidationError

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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            food_item = FoodItem.objects.select_for_update().get(pk=self.food_item_id)
            self.quantity = int(self.quantity)
            if food_item.quantity < self.quantity:
                raise ValidationError('Food item quantity is less than the collection quantity')
            food_item.quantity -= self.quantity
            food_item.save()
            super().save(*args, **kwargs)
