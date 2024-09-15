import django_filters
from rest_framework import serializers

from authentication.serializers import DriverSerializer
from core.serializers import CitySerializer
from .models import Post




class GETPostSerializer(serializers.ModelSerializer):
    to_city = CitySerializer(many=False, read_only=False)
    from_city = CitySerializer(many=False, read_only=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'description',
            'from_city',
            'from_address_line',
            'pickup_time',
            'to_city',
            'to_address_line',
            'arrival_time',
            'max_weight',
            'max_size',
            'created_by'
        ]


class POSTPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'description',
            'from_city',
            'from_address_line',
            'pickup_time',
            'to_city',
            'to_address_line',
            'arrival_time',
            'max_weight',
            'max_size',
            'created_by'
        ]
