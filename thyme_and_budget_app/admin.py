from django.contrib import admin
from .models.collectionModel import Collection
from .models.locationModel import Location
from .models.foodModel import FoodItem

# Register your models here.
admin.site.register(Collection)
admin.site.register(Location)
admin.site.register(FoodItem)
