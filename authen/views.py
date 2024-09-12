from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Client

from .serializers import (
    UserSerializer, 
    ClientSerializer, 
    DriverSerializer, 
    DriverPhoneNumberSerializer, 
    CarSerializer, 
    CarImageSerializer, 
    CarLicenseSerializer, 
    NationalityIDSerializer, 
    DriverLicenseSerializer
)
from .models import (
    Driver, 
    DriverPhoneNumber, 
    Car, 
    CarImage, 
    CarLicense, 
    NationalityID, 
    DriverLicense
)

# View to handle user login and generate token

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
def register_client(request):
    client_data = request.data.get('client', {})
    
    # Extract and validate user details from client_data
    username = client_data.get('username')
    email = client_data.get('email')
    password = client_data.get('password')
    first_name = client_data.get('first_name', '')  # Optional fields
    last_name = client_data.get('last_name', '')    # Optional fields
    
    if not all([username, email, password]):
        return Response({"detail": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
    except IntegrityError:
        return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Add user ID to client data
    client_data['user'] = user.id
    client_serializer = ClientSerializer(data=client_data)
    
    if client_serializer.is_valid():
        client = client_serializer.save()
        
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        # Prepare response data
        response_data = {
            'token': token.key,
            'client': client_serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    # Rollback user creation if client data is invalid
    user.delete()
    return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_driver(request):
    # Serialize and save the Driver instance
    driver_serializer = DriverSerializer(data=request.data)
    if driver_serializer.is_valid():
        try:
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
        except IntegrityError:
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        driver = driver_serializer.save(user=user)
        
        # Save related data and handle errors

        phone_number_data = request.data.get('phone_number', {})
        phone_number_data['driver'] = driver.id
        phone_number_serializer = DriverPhoneNumberSerializer(data=phone_number_data)
        if not phone_number_serializer.is_valid():
            driver.delete()  # Rollback driver creation
            user.delete()  # Rollback user creation
            return Response(phone_number_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        phone_number_serializer.save()

        license_data = request.data.get('license', {})
        license_data['driver'] = driver.id
        license_serializer = DriverLicenseSerializer(data=license_data)
        if not license_serializer.is_valid():
            driver.delete() 
            user.delete()  
            phone_number_serializer.instance.delete()  
            return Response(license_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        license_serializer.save()

        car_data = request.data.get('cars', [])
        for car in car_data:
            car['driver'] = driver.id
            car_serializer = CarSerializer(data=car)
            if not car_serializer.is_valid():
                driver.delete()  
                user.delete() 
                phone_number_serializer.instance.delete()  
                license_serializer.instance.delete() 
                return Response(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            car_serializer.save()

        car_images_data = request.data.get('car_images', [])
        for car_image in car_images_data:
            car_image_serializer = CarImageSerializer(data=car_image)
            if not car_image_serializer.is_valid():
                driver.delete()  
                user.delete()  
                phone_number_serializer.instance.delete() 
                license_serializer.instance.delete()  
                Car.objects.filter(driver=driver).delete()  
                return Response(car_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            car_image_serializer.save()

        car_licenses_data = request.data.get('car_licenses', [])
        for car_license in car_licenses_data:
            car_license['car'] = car_license.get('car')  
            car_license_serializer = CarLicenseSerializer(data=car_license)
            if not car_license_serializer.is_valid():
                driver.delete() 
                user.delete() 
                phone_number_serializer.instance.delete() 
                license_serializer.instance.delete() 
                Car.objects.filter(driver=driver).delete()  
                CarImage.objects.filter(car__driver=driver).delete() 
                return Response(car_license_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            car_license_serializer.save()

        nationality_ids_data = request.data.get('nationality_ids', [])
        for nationality_id in nationality_ids_data:
            nationality_id['driver'] = driver.id
            nationality_id_serializer = NationalityIDSerializer(data=nationality_id)
            if not nationality_id_serializer.is_valid():
                driver.delete() 
                user.delete()  
                phone_number_serializer.instance.delete() 
                license_serializer.instance.delete()  
                Car.objects.filter(driver=driver).delete() 
                CarImage.objects.filter(car__driver=driver).delete() 
                CarLicense.objects.filter(car__driver=driver).delete()  
                return Response(nationality_id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            nationality_id_serializer.save()

        # Generate and return the token
        token, created = Token.objects.get_or_create(user=user)
        
        # Prepare response data
        response_data = {
            'token': token.key,
            'driver': driver_serializer.data,
            'phone_number': phone_number_serializer.data,
            'license': license_serializer.data,
            'cars': CarSerializer(Car.objects.filter(driver=driver), many=True).data,
            'car_images': CarImageSerializer(CarImage.objects.filter(car__driver=driver), many=True).data,
            'car_licenses': CarLicenseSerializer(CarLicense.objects.filter(car__driver=driver), many=True).data,
            'nationality_ids': NationalityIDSerializer(NationalityID.objects.filter(driver=driver), many=True).data
        }

        return Response(response_data)
    
    return Response(driver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# View to test token authentication
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
