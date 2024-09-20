from django.contrib import admin

from core.models import City, Government, PhoneNumber, NationalityID, DriverLicense, CarLicense, Car, CarImage, \
    DeliveryFEESettings

# Register your core_models here.

admin.site.register(City)
admin.site.register(Government)
admin.site.register(PhoneNumber)
admin.site.register(NationalityID)
admin.site.register(DriverLicense)
admin.site.register(CarLicense)
admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(DeliveryFEESettings)
