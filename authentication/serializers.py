from rest_framework import serializers

from authentication.models import Client, Driver, BaseUser
from core.models import City, PhoneNumber, Car, DriverLicense, NationalityID, UserType


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class ClientRegisterSerializer(serializers.ModelSerializer):
    city_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    phone_numbers = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Client
        fields = ['email', 'first_name', 'last_name', 'password', 'name', 'city_ids', 'phone_numbers',
                  'address_line', 'birth_date']

    def create(self, validated_data):
        # Extract related fields
        city_ids = validated_data.pop('city_ids', [])
        phone_numbers = validated_data.pop('phone_numbers', [])

        # Create the base user
        user = Client.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=UserType.CLIENT,
            name=validated_data['name'],
            address_line=validated_data['address_line'],
            birth_date=validated_data['birth_date'],
        )
        # Add cities
        cities = City.objects.filter(id__in=city_ids)
        user.city_ids.set(cities)

        # Add phone numbers (create new ones if they don't exist)
        for number in phone_numbers:
            phone, created = PhoneNumber.objects.get_or_create(phone_number=number)
            user.phone_numbers.add(phone)

        user.save()
        return user


class DriverRegisterSerializer(serializers.ModelSerializer):
    city_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    phone_numbers = serializers.ListField(child=serializers.CharField(), write_only=True)
    car_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    driver_license_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Driver
        fields = ['email', 'name', 'first_name', 'last_name', 'password', 'name', 'city_ids', 'phone_numbers', 'address_line',
                  'birth_date', 'nationality_id', 'car_ids', 'driver_license_ids']

    def create(self, validated_data):
        # Extract related fields
        city_ids = validated_data.pop('city_ids', [])
        phone_numbers = validated_data.pop('phone_numbers', [])
        car_ids = validated_data.pop('car_ids', [])
        driver_license_ids = validated_data.pop('driver_license_ids', [])

        # Create the base user
        user = Driver.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=UserType.DRIVER,
            name=validated_data['name'],
            address_line=validated_data['address_line'],
            birth_date=validated_data['birth_date'],
            nationality_id=NationalityID.objects.get(id=validated_data['nationality_id']),
        )

        # Add cities
        cities = City.objects.filter(id__in=city_ids)
        user.city_id.set(cities)

        # Add phone numbers (create new ones if they don't exist)
        for number in phone_numbers:
            phone, created = PhoneNumber.objects.get_or_create(number=number)
            user.phone_numbers.add(phone)

        # Add cars
        cars = Car.objects.filter(id__in=car_ids)
        user.car_id.set(cars)

        # Add driver licenses
        licenses = DriverLicense.objects.filter(id__in=driver_license_ids)
        user.driver_license_id.set(licenses)

        user.save()
        return user
