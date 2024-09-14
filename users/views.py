from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import Driver, Client
from authentication.serializers import DriverSerializer, ClientSerializer


# Create your views here.

# DRIVER CRUD
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated, ))
def listDrivers(request):
    try:
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response({
            'status': 'success',
            'message': 'success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'message': str(e),
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


class DriverProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            driver = Driver.objects.get(id=id)
            serializer = DriverSerializer(driver)
            return Response({
                'status': 'success',
                'message': 'success',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            driver = Driver.objects.get(id=id)
            serializer = DriverSerializer(driver, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'driver updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'driver not updated, data is not valid',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            driver = Driver.objects.get(id=id)
            driver.delete()

            return Response({
                'status': 'success',
                'message': 'driver deleted successfully',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


# CLIENT CRUD
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated, ))
def listClients(request):
    try:
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response({
            'status': 'success',
            'message': 'success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'message': str(e),
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


class ClientProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
            serializer = ClientSerializer(client)
            return Response({
                'status': 'success',
                'message': 'success',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            client = Client.objects.get(id=id)
            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'client updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'client not updated, data is not valid',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            client = Client.objects.get(id=id)
            client.delete()

            return Response({
                'status': 'success',
                'message': 'client deleted successfully',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
