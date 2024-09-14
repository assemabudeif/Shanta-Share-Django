# from django.db import core_models
# from core.core_models import Client , Driver
#
#
# @property
# def age(self):
#     from datetime import date
#     today = date.today()
#     return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
#
#
# class DriverPhoneNumber(core_models.Model):
#     driver = core_models.OneToOneField(Driver, on_delete=core_models.CASCADE, unique=True)
#     phone_number = core_models.CharField(max_length=15)
#
#     def __str__(self):
#         return f"Phone number for Driver {self.driver.name}"
#
# class ClientPhoneNumber(core_models.Model):
#     client = core_models.ForeignKey(Client, on_delete=core_models.CASCADE)
#     phone_number = core_models.CharField(max_length=15)
#
#     def __str__(self):
#         return f"Phone number for Client {self.client.name}"
#
# class Car(core_models.Model):
#     driver = core_models.ForeignKey(Driver, on_delete=core_models.CASCADE)
#     make = core_models.CharField(max_length=100,null=True)
#     model = core_models.CharField(max_length=100)
#     year = core_models.IntegerField(null=True)
#
#     def __str__(self):
#         return f"{self.make} {self.model} ({self.year})"
#
# class CarImage(core_models.Model):
#     car = core_models.ForeignKey(Car, on_delete=core_models.CASCADE)
#     image_url = core_models.TextField()
#
#     def __str__(self):
#         return f"Image for Car {self.car.id}"
#
# class DriverLicense(core_models.Model):
#     driver = core_models.ForeignKey(Driver, on_delete=core_models.CASCADE)
#     license_number = core_models.CharField(max_length=100)
#     issued_date = core_models.DateField(null=True)
#     expiration_date = core_models.DateField(null=True)
#     front_image_url = core_models.TextField()
#     back_image_url = core_models.TextField()
#
#     def __str__(self):
#         return f"License {self.license_number} for Driver {self.driver.name}"
#
# class CarLicense(core_models.Model):
#     car = core_models.ForeignKey(Car, on_delete=core_models.CASCADE)
#     license_number = core_models.CharField(max_length=100)
#     issued_date = core_models.DateField(null=True)
#     expiration_date = core_models.DateField(null=True)
#     front_image_url = core_models.TextField()
#     back_image_url = core_models.TextField()
#
#     def __str__(self):
#         return f"License {self.license_number} for Car {self.car.id}"
#
# class NationalityID(core_models.Model):
#     driver = core_models.ForeignKey(Driver, on_delete=core_models.CASCADE)
#     nationality_id_number = core_models.CharField(max_length=100)
#     issued_date = core_models.DateField(null=True)
#     expiration_date = core_models.DateField(null=True)
#     front_image_url = core_models.TextField()
#     back_image_url = core_models.TextField()
#
#     def __str__(self):
#         return f"Nationality ID {self.nationality_id_number} for Driver {self.driver.name}"
#
#
#
#
#
#
#
#
#
