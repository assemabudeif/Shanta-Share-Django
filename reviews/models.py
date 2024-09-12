from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import Client, Driver

# from core.models import Client, Driver

# Create your models here.

class Review(models.Model):
    id=models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(validators=[ MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f'Review {self.id} - Rating: {self.rating}'