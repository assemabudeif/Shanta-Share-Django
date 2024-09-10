from django.db import models

# Create your models here.

class Government(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class City(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    government = models.ForeignKey('Government', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Driver(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    birth_date = models.DateField()
    address_line = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Client(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address_line = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    delivery_address_line = models.CharField(max_length=255)
    pickup_address_line = models.CharField(max_length=255)
    delivery_city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='delivery_orders')
    pickup_city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='pickup_orders')

    def __str__(self):
        return f'Order {self.id} - Status: {self.status}'