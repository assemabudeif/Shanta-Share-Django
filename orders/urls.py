from django.contrib import admin
from django.urls import path, include

from orders.views import ClientOrderView, get_driver_orders, get_driver_single_order, \
    update_order_status, get_post_orders, AdminOrdersView, GetClientsOrdersView, GetDriverOrdersView, \
    GetAdminOrdersView, withdraw_driver_earnings, complete_order

urlpatterns = [
    # Client Urls
    path('client/', ClientOrderView.as_view(), name='client-orders'),
    # path('client-orders/', get_clients_orders, name='client-orders'),
    path('client-orders/', GetClientsOrdersView.as_view(), name='client-orders'),
    path('client/complete-order', complete_order, name='client-complete'),

    # Driver Urls
    # path('driver-orders/', get_driver_orders, name='driver-orders'),
    path('driver-orders/', GetDriverOrdersView.as_view(), name='driver-orders'),
    path('driver-single-order/', get_driver_single_order, name='driver-single-order'),
    path('update-status/', update_order_status, name='update-status'),
    path('post-orders/', get_post_orders, name='post-orders'),
    path('withdraw', withdraw_driver_earnings, name='withdraw-driver-earnings'),

    # Admin Urls
    path('admin/', AdminOrdersView.as_view(), name='admin-orders'),
    path('admin/orders', GetAdminOrdersView.as_view(), name='admin-orders-pagination'),
]
