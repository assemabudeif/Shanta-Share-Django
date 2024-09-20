from django.contrib import admin
from django.urls import path, include

from orders.views import get_clients_orders, ClientOrderView, get_driver_orders, get_driver_single_order, \
    update_order_status, get_post_orders, AdminOrdersView

urlpatterns = [
    # Client Urls
    path('client/', ClientOrderView.as_view(), name='client-orders'),
    path('client-orders/', get_clients_orders, name='client-orders'),

    # Driver Urls
    path('driver-orders/', get_driver_orders, name='driver-orders'),
    path('driver-single-order/', get_driver_single_order, name='driver-single-order'),
    path('update-status/', update_order_status, name='update-status'),
    path('post-orders/', get_post_orders, name='post-orders'),

    # Admin Urls
    path('admin/', AdminOrdersView.as_view(), name='admin-orders'),
]
