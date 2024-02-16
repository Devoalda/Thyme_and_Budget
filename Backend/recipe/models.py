from django.db import models
from django.conf import settings

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cooking_time = models.IntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title