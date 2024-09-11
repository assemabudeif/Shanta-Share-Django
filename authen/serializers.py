from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Driver
from .models import Client, ClientPhoneNumber
from rest_framework import serializers
from .models import Driver
from .models import DriverLicense
from .models import DriverLicense
from .models import Driver, DriverPhoneNumber, Car, CarImage, CarLicense, NationalityID

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



   # ==========   Driver Serializers  ==========



class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'average_rating', 'birth_date', 'address_line', 'city']



class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = ['id', 'driver', 'license_number', 'issued_date', 'expiration_date', 'front_image_url', 'back_image_url']


class DriverLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverLicense
       
        fields = ['id', 'driver', 'license_number', 'issued_date', 'expiration_date', 'front_image_url', 'back_image_url']


class DriverPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverPhoneNumber
        fields = ['id', 'driver', 'phone_number']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'driver', 'make', 'model', 'year']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'car', 'image_url']


class CarLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLicense
        fields = ['id', 'car', 'license_number', 'issued_date', 'expiration_date', 'front_image_url', 'back_image_url']

class NationalityIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalityID
        fields = ['id', 'driver', 'nationality_id_number', 'issued_date', 'expiration_date', 'front_image_url', 'back_image_url']        



# ==========   Client Serializers  ==========



class ClientPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPhoneNumber
        fields = ['id', 'phone_number']

class ClientSerializer(serializers.ModelSerializer):
    phone_numbers = ClientPhoneNumberSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'name', 'address_line', 'city', 'phone_numbers']

    def create(self, validated_data):
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        client = Client.objects.create(**validated_data)
        for phone_number_data in phone_numbers_data:
            ClientPhoneNumber.objects.create(client=client, **phone_number_data)
        return client

    def update(self, instance, validated_data):
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        instance.name = validated_data.get('name', instance.name)
        instance.address_line = validated_data.get('address_line', instance.address_line)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        # Update phone numbers
        existing_phone_numbers = {phone_number.id: phone_number for phone_number in instance.phone_numbers.all()}
        for phone_number_data in phone_numbers_data:
            phone_number_id = phone_number_data.get('id')
            if phone_number_id:
                phone_number = existing_phone_numbers.pop(phone_number_id)
                phone_number.phone_number = phone_number_data.get('phone_number', phone_number.phone_number)
                phone_number.save()
            else:
                ClientPhoneNumber.objects.create(client=instance, **phone_number_data)

        # Delete removed phone numbers
        for phone_number in existing_phone_numbers.values():
            phone_number.delete()

        return instance