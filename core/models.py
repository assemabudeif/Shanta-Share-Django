from django.db import models
from django.contrib.auth.models import User


class Government(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    government = models.ForeignKey(Government, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    birth_date = models.DateField()
    address_line = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
     return self.name

  

class Client(models.Model):
    name = models.CharField(max_length=255)
    address_line = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
     return self.name