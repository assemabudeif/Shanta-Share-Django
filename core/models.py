from django.db import models

class UserType(models.TextChoices):
    DRIVER = 'DRIVER'
    CLIENT = 'CLIENT'
    ADMIN = 'ADMIN'

class Government(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    government = models.ForeignKey(Government, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, to=User, field_name='phone_number')
    phone_number = models.CharField(max_length=255)


class NationalityID(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    nationality_id_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.TextField()
    back_image_url = models.TextField()


class DriverLicense(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.TextField()
    back_image_url = models.TextField()


class Car(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()


class CarLicense(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.TextField()
    back_image_url = models.TextField()


class CarImage(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    image_url = models.TextField()

# class Driver(core_models.Model):
#     user = core_models.OneToOneField(User, on_delete=core_models.CASCADE, null=True, blank=True)
#     name = core_models.CharField(max_length=255)
#     average_rating = core_models.DecimalField(max_digits=3, decimal_places=2)
#     birth_date = core_models.DateField()
#     address_line = core_models.CharField(max_length=255)
#     city = core_models.ForeignKey(City, on_delete=core_models.CASCADE)
#
#     def __str__(self):
#      return self.name
#
#
#
# class Client(core_models.Model):
#     name = core_models.CharField(max_length=255)
#     address_line = core_models.CharField(max_length=255)
#     city = core_models.ForeignKey(City, on_delete=core_models.CASCADE)
#
#     def __str__(self):
#      return self.name
