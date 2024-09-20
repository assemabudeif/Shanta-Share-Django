from rest_framework import serializers

from core.models import City, Government, PhoneNumber, NationalityID, DriverLicense, CarLicense, Car, CarImage
from drf_extra_fields.fields import Base64ImageField


class GovernmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Government
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    government = GovernmentSerializer()

    class Meta:
        model = City
        fields = '__all__'


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'


class NationalityIDSerializer(serializers.ModelSerializer):
    front_image_url = Base64ImageField(required=True)
    back_image_url = Base64ImageField(required=True)

    class Meta:
        model = NationalityID
        fields = '__all__'


class CarLicenseSerializer(serializers.ModelSerializer):
    front_image_url = Base64ImageField(required=True)
    back_image_url = Base64ImageField(required=True)

    class Meta:
        model = CarLicense
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    image_url = Base64ImageField(required=True)

    class Meta:
        model = CarImage
        fields = '__all__'


class DriverLicenseSerializer(serializers.ModelSerializer):
    front_image_url = Base64ImageField(required=True)
    back_image_url = Base64ImageField(required=True)

    class Meta:
        model = DriverLicense
        fields = '__all__'
