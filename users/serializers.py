from rest_framework import serializers
from authentication.models import Driver, Client
from core.serializers import CitySerializer, PhoneNumberSerializer, CarSerializer, DriverLicenseSerializer, \
    NationalityIDSerializer


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

    city_ids = CitySerializer(many=True, read_only=True)  # Accepting nested City objects
    phone_numbers = PhoneNumberSerializer(read_only=True, many=True)
    car_ids = CarSerializer(read_only=True, many=True)
    driver_license_ids = DriverLicenseSerializer(read_only=True, many=True)
    nationality_id = NationalityIDSerializer(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    city_ids = CitySerializer(many=True, read_only=True)  # Accepting nested City objects
    phone_numbers = PhoneNumberSerializer(read_only=True, many=True)