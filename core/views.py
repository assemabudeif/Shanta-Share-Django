from django.shortcuts import render
from rest_framework import generics
from django_filters import rest_framework as filters

from core.models import Government, City
from core.serializers import GovernmentSerializer, CitySerializer


# Create your views here.
class GovernmentListCreateView(generics.ListCreateAPIView):
    queryset = Government.objects.all()
    serializer_class = GovernmentSerializer


class GovernmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Government.objects.all()
    serializer_class = GovernmentSerializer


# City FilterSet to filter by government_id
class CityFilter(filters.FilterSet):
    government_id = filters.NumberFilter(field_name='government__id')

    class Meta:
        model = City
        fields = ['government_id']


class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_class = CityFilter


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer