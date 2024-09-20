from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from authentication.models import Client, Driver, BaseUser
from core.models import City, PhoneNumber, Car, DriverLicense, NationalityID, UserType, Government
from core.serializers import CitySerializer, PhoneNumberSerializer, CarSerializer, DriverLicenseSerializer, \
    NationalityIDSerializer


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        # fields = ['id', 'name', 'city_ids', 'phone_numbers', 'address_line', 'birth_date', 'average_rating', 'nationality_id', 'car_ids', 'driver_license_ids', 'user']

    city_ids = CitySerializer(many=True, read_only=True)  # Accepting nested City objects
    phone_numbers = PhoneNumberSerializer(read_only=True, many=True)
    car_ids = CarSerializer(read_only=True, many=True)
    driver_license_ids = DriverLicenseSerializer(read_only=True, many=True)
    nationality_id = NationalityIDSerializer(read_only=True)
    user = BaseUserSerializer(read_only=True)
    profile_picture = Base64ImageField(required=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    city_ids = CitySerializer(many=True, read_only=True)  # Accepting nested City objects
    phone_numbers = PhoneNumberSerializer(read_only=True, many=True)
    profile_picture = Base64ImageField(required=True)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            'username',
            'password',
            'user_type',
            'admin',
            'is_superuser',
        ]

    def create(self, validated_data):
        user = BaseUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            user_type=UserType.ADMIN,
            admin=True,
            is_superuser=True
        )
        return user


class ClientRegisterSerializer(serializers.ModelSerializer):
    # city_ids = serializers.ListField(child=CitySerializer(), write_only=True)
    # city_ids = CitySerializer(many=True, write_only=True)  # Accepting nested City objects
    city_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    phone_numbers = serializers.ListField(child=PhoneNumberSerializer(), write_only=True)
    profile_picture = Base64ImageField(required=True)

    class Meta:
        model = Client
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'name',
            'city_ids',
            'phone_numbers',
            'address_line',
            'birth_date',
            'profile_picture',
        ]

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
            profile_picture=validated_data['profile_picture'],
        )

        # Add or create cities
        cities = City.objects.filter(id__in=city_ids)
        user.city_ids.set(cities)
        # for city_data in city_ids:
        #     government, created = Government.objects.get_or_create(
        #         name=city_data['government']['name'],
        #     )
        #     city, created = City.objects.get_or_create(
        #         name=city_data['name'],
        #         government=government,
        #     )
        #     user.city_ids.add(city)

        # Add phone numbers (create new ones if they don't exist)
        for number in phone_numbers:
            phone, created = PhoneNumber.objects.get_or_create(phone_number=number['phone_number'])
            user.phone_numbers.add(phone)

        user.save()
        return user


class DriverRegisterSerializer(serializers.ModelSerializer):
    city_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    phone_numbers = serializers.ListField(child=PhoneNumberSerializer(), write_only=True)
    car_ids = serializers.ListField(child=CarSerializer(), write_only=True)
    driver_license_ids = serializers.ListField(child=DriverLicenseSerializer(), write_only=True)
    nationality_id = NationalityIDSerializer(write_only=True)
    profile_picture = Base64ImageField(required=True)

    class Meta:
        model = Driver
        fields = [
            'email',
            'name',
            'first_name',
            'last_name',
            'password',
            'name',
            'city_ids',
            'phone_numbers',
            'address_line',
            'birth_date',
            'nationality_id',
            'car_ids',
            'driver_license_ids',
            'profile_picture',
        ]

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
            profile_picture=validated_data['profile_picture'],
        )

        # Add cities
        cities = City.objects.filter(id__in=city_ids)
        user.city_ids.set(cities)

        # Add phone numbers (create new ones if they don't exist)
        for number in phone_numbers:
            phone, created = PhoneNumber.objects.get_or_create(phone_number=number['phone_number'])
            user.phone_numbers.add(phone)

        # Add cars
        for car_data in car_ids:
            car, created = Car.objects.get_or_create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
            )
            user.car_ids.add(car)

        # Add driver licenses
        for license_data in driver_license_ids:
            driver_license, created = DriverLicense.objects.get_or_create(
                license_number=license_data['license_number'],
                issued_date=license_data['issued_date'],
                front_image_url=license_data['front_image_url'],
                back_image_url=license_data['back_image_url'],
                expiration_date=license_data['expiration_date'],
            )
            user.driver_license_ids.add(driver_license)

        # Add nationality id
        nationality_id = validated_data.pop('nationality_id', None)
        if nationality_id:
            user.nationality_id = NationalityID.objects.create(
                nationality_id_number=nationality_id['nationality_id_number'],
                issued_date=nationality_id['issued_date'],
                expiration_date=nationality_id['expiration_date'],
                front_image_url=nationality_id['front_image_url'],
                back_image_url=nationality_id['back_image_url'],
            )

        user.save()
        return user
