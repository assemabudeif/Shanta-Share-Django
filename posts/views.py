import django_filters
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import City, DeliveryFEESettings
from core.pagination import StanderPagination
from .models import Post
from .serializers import GETPostSerializer, serializers, POSTPostSerializer
import requests


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = GETPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = POSTPostSerializer(data=request_data)
        if request.user.is_authenticated:
            request_data["created_by"] = request.user.id
        else:
            return Response(serializer.data, status)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass

    # def perform_create(self, serializer):
    #     if not hasattr(self.request.user, 'driver'):
    #         raise serializers.ValidationError('Only drivers can create posts.')
    #
    #     serializer.save(created_by=self.request.user.driver)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = GETPostSerializer


class PostFilter(django_filters.FilterSet):
    # pickup_time = django_filters.DateTimeFilter()
    # arrival_time = django_filters.DateTimeFilter()

    from_city = django_filters.NumberFilter(field_name='from_city__id', lookup_expr='exact')
    to_city = django_filters.NumberFilter(field_name='to_city__id', lookup_expr='exact')

    from_government = django_filters.NumberFilter(field_name='from_city__government__id', lookup_expr='exact')
    to_government = django_filters.NumberFilter(field_name='to_city__government__id', lookup_expr='exact')

    # from_city = django_filters.CharFilter(field_name='from_city__name', lookup_expr='icontains')
    # to_city = django_filters.CharFilter(field_name='to_city__name', lookup_expr='icontains')
    #
    # from_government = django_filters.CharFilter(field_name='from_city__government__name', lookup_expr='icontains')
    # to_government = django_filters.CharFilter(field_name='to_city__government__name', lookup_expr='icontains')
    # to_government = django_filters.NumberFilter(field_name='to_city__government__id', lookup_expr='exact')

    max_weight = django_filters.NumberFilter(field_name='max_weight', lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name='max_size', lookup_expr='gte')

    class Meta:
        model = Post
        fields = ['from_city', 'to_city', 'from_government', 'to_government', 'description', 'max_weight', 'max_size']


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = GETPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    pagination_class = StanderPagination

    # filterset_fields = ['from_city', 'to_city', 'pickup_time', 'arrival_time']
    search_fields = ['description', 'from_address_line', 'to_address_line', 'created_by__username']
    ordering_fields = ['pickup_time', 'arrival_time']


class PostDetailsView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = GETPostSerializer


def calculate_delivery_fees(request):
    delivery_fees_settings = DeliveryFEESettings.load()

    city1 = City.objects.filter(id=request.GET.get('city1_id')).first()
    city2 = City.objects.filter(id=request.GET.get('city2_id')).first()

    max_weight = float(request.GET.get('max_weight'))
    max_size = float(request.GET.get('max_size'))
    distance = get_here_route_distance(city1, city2)

    delivery_fees = (
        (distance * delivery_fees_settings.distance_factor) +
        (distance * delivery_fees_settings.distance_factor) * (max_weight * delivery_fees_settings.weight_factor) +
        (distance * delivery_fees_settings.distance_factor) * (max_size * delivery_fees_settings.size_factor)
    )

    return JsonResponse({'delivery_fees': delivery_fees})


def get_here_route_distance(city1, city2):
    here_api_key = 'YOUR_HERE_API_KEY'  # Replace with your actual Here Maps API key
    url = "https://router.hereapi.com/v8/routes"

    # Request parameters
    params = {
        'apikey': 'LJogNFnKbldU9zjSgP1QIzfhm0W2BmcWIsn3qbo7v8Q',
        'transportMode': 'car',
        'origin': f'{city1.latitude},{city1.longitude}',  # Origin coordinates
        'destination': f'{city2.latitude},{city2.longitude}',  # Destination coordinates
        'return': 'summary',  # We want a summary, including the distance
    }

    # Send a GET request to the Here Maps API
    response = requests.get(url, params=params)

    # If the response is successful, parse the JSON data
    if response.status_code == 200:
        data = response.json()
        # Extract the distance (in meters) from the first route's summary
        distance = data['routes'][0]['sections'][0]['summary']['length'] / 1000  # Convert meters to kilometers
        return distance

    # If something goes wrong, return None
    return None
