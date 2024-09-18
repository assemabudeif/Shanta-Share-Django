from django.db import models


class Singleton(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override save to ensure only one instance with pk=1."""
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of the singleton instance."""
        pass

    @classmethod
    def load(cls):
        """Load the singleton instance, or create it if not found."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


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
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, to=User, field_name='phone_number')
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.phone_number


class NationalityID(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    nationality_id_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.ImageField(upload_to='Nationality_id_images')
    back_image_url = models.ImageField(upload_to='Nationality_id_images')

    def __str__(self):
        return self.nationality_id_number


class DriverLicense(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.ImageField(upload_to='Car_license_images')
    back_image_url = models.ImageField(upload_to='Car_license_images')

    def __str__(self):
        return self.license_number


class Car(models.Model):
    # driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.make


class CarLicense(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiration_date = models.DateField()
    front_image_url = models.ImageField(upload_to='Driver_license_images')
    back_image_url = models.ImageField(upload_to='Driver_license_images')

    def __str__(self):
        return self.license_number


class CarImage(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='Car_images')

    def __str__(self):
        return self.image_url


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


class DeliveryFEESettings(Singleton):
    distance_factor = models.FloatField()
    type_factor = models.FloatField()
    weight_factor = models.FloatField()
    size_factor = models.FloatField()

    def __str__(self):
        return f"Settings ({self.pk})"
