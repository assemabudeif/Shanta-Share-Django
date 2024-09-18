from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# from django.contrib.auth import login

from .models import BaseUser, Driver, Client
from .serializers import ClientSerializer, ClientRegisterSerializer, DriverRegisterSerializer


# Create your views here.
@api_view(['POST'])
def client_login(request):
    try:
        user = Client.objects.get(username=request.data['email'])

        if not user.check_password(request.data['password']):
            return Response({
                "status": "error",
                "message": "Invalid password.",
            },
                status=status.HTTP_400_BAD_REQUEST)
        user.last_login = datetime.now()
        user.save()
        serializer = ClientSerializer(instance=user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'message': 'Logged in successfully.',
            'client': serializer.data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        },
            status=status.HTTP_200_OK)
    except Client.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "status": "error",
            "message": "An error occurred. Please try again.",
            "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def driver_login(request):
    try:
        user = Driver.objects.get(username=request.data['email'])

        if not user.check_password(request.data['password']):
            return Response({
                "status": "error",
                "message": "Invalid password.",
            },
                status=status.HTTP_400_BAD_REQUEST)
        user.last_login = datetime.now()
        user.save()
        serializer = ClientSerializer(instance=user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'message': 'Logged in successfully.',
            'driver': serializer.data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        },
            status=status.HTTP_200_OK)
    except Driver.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "status": "error",
            "message": "An error occurred. Please try again.",
            "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST)


class ClientRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Registered successfully.',
                'client': serializer.data,
                'city_ids': serializer.validated_data['city_ids'],
                'phone_numbers': serializer.validated_data['phone_numbers'],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DriverRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Registered successfully.',
                'driver': serializer.data,
                'city_ids': serializer.validated_data['city_ids'],
                'phone_numbers': serializer.validated_data['phone_numbers'],
                'car_ids': serializer.validated_data['car_ids'],
                # 'driver_license_ids': serializer.validated_data['driver_license_ids'],
                # 'nationality_id': serializer.validated_data['nationality_id'],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)