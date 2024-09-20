from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import (
    NationalityID,
    Car,
    DriverLicense,
    CarLicense,
    City,
    PhoneNumber,
    UserType,
)


# Create your core_models here.
class BaseUser(AbstractUser):
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.CLIENT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)  # a superuser

    # username = email

    def __str__(self):
        return self.email


class Client(BaseUser):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="client",
    )
    name = models.CharField(max_length=255)
    city_ids = models.ManyToManyField(City)
    phone_numbers = models.ManyToManyField(PhoneNumber)
    address_line = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", null=False, blank=True
    )

    @property
    def age(self):
        from datetime import date

        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"


class Driver(BaseUser):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="driver",
    )
    name = models.CharField(max_length=255)
    city_ids = models.ManyToManyField(City)
    phone_numbers = models.ManyToManyField(PhoneNumber)
    address_line = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    nationality_id = models.OneToOneField(
        NationalityID, null=True, on_delete=models.CASCADE
    )
    car_ids = models.ManyToManyField(Car, null=True)
    driver_license_ids = models.ManyToManyField(DriverLicense, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", null=False, blank=True
    )

    @property
    def age(self):
        from datetime import date

        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    class Meta:
        verbose_name = "Driver"

    def __str__(self):
        return self.name
