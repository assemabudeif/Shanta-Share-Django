from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from posts.models import Post
from django.http import JsonResponse
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsDriverOrClient
from rest_framework.decorators import api_view
from .models import  Client, Driver


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsDriverOrClient]

    def get_queryset(self):
        # Filter reviews by the driver's ID
        user = self.request.user
        driver = getattr(user, 'driver', None)
        driver_id = self.request.query_params.get('driver_id', None)

        if driver_id :
            return Review.objects.filter(driver_id=driver_id)
        
        elif driver:
            # Return only reviews related to the logged-in driver
            return Review.objects.filter(driver=driver)
        
            # If the user is not a driver, return an empty queryset
        else:
            return Review.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        client = getattr(user, 'client', None)
        driver = getattr(user, 'driver', None)

        # Save the review with either the client or driver
        if client:
            serializer.save(client=client)
        elif driver:
            serializer.save(driver=driver)
        else:
            # Handle the case where the user is neither a client nor a driver
            serializer.save()

# =====================calculate totale posts, orders and users================


api_view(['GET'])
def get_totals(request):

    total_orders = Order.objects.count()
    total_posts = Post.objects.count()
    total_clients = Client.objects.count()  
    total_drivers = Driver.objects.count()
    data={
        'orders': total_orders,
        'posts': total_posts,
        'clients': total_clients,
        'drivers': total_drivers,
    }
    return JsonResponse(data)
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def get_annual_statistics(request):
    stats = []
    for month in range(1, 13):  
        orders_count = Order.objects.filter(created_at__month=month).count()
        posts_count = Post.objects.filter(created_at__month=month).count()
        clients_count = Client.objects.filter(date_joined__month=month).count()
        drivers_count = Driver.objects.filter(date_joined__month=month).count()
        
        stats.append({
            'name': months[month-1],
            'orders': orders_count,
            'posts': posts_count,
            'clients': clients_count,
            'drivers': drivers_count,
        })

    return JsonResponse(stats, safe=False)