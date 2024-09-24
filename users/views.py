from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import Driver, Client
from authentication.serializers import DriverSerializer, ClientSerializer
from core.models import UserType
from core.pagination import StanderPagination


# Create your views here.

# DRIVER CRUD
class ListDriversView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = ClientSerializer
    pagination_class = StanderPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == UserType.ADMIN:
            return self.list(request, *args, **kwargs)
        else:
            return Response({
                "status": "error",
                "message": "Only admins can see their orders"
            }, status=status.HTTP_403_FORBIDDEN)


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
class ListClientsView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = StanderPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == UserType.ADMIN:
            return self.list(request, *args, **kwargs)
        else:
            return Response({
                "status": "error",
                "message": "Only admins can see their orders"
            }, status=status.HTTP_403_FORBIDDEN)

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
