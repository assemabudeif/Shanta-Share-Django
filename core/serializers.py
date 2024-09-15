from rest_framework import serializers

from core.models import City, Government, PhoneNumber, NationalityID, DriverLicense, CarLicense, Car, CarImage


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
    class Meta:
        model = NationalityID
        fields = '__all__'


class CarLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLicense
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'


class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = '__all__'
