from django.db import models
from core.models import Client , Driver


@property
def age(self):
    from datetime import date
    today = date.today()
    return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class DriverPhoneNumber(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Phone number for Driver {self.driver.name}"

class ClientPhoneNumber(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Phone number for Client {self.client.name}"

class Car(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    make = models.CharField(max_length=100,null=True)
    model = models.CharField(max_length=100)
    year = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image_url = models.TextField()

    def __str__(self):
        return f"Image for Car {self.car.id}"

class DriverLicense(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    front_image_url = models.TextField()
    back_image_url = models.TextField()

    def __str__(self):
        return f"License {self.license_number} for Driver {self.driver.name}"

class CarLicense(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    front_image_url = models.TextField()
    back_image_url = models.TextField()

    def __str__(self):
        return f"License {self.license_number} for Car {self.car.id}"

class NationalityID(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    nationality_id_number = models.CharField(max_length=100)
    issued_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    front_image_url = models.TextField()
    back_image_url = models.TextField()

    def __str__(self):
        return f"Nationality ID {self.nationality_id_number} for Driver {self.driver.name}"







