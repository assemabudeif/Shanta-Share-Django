from django.urls import path, include
from .views import generate_iframe, payment_callback

urlpatterns = [
    path('iframe', generate_iframe),
    path('callback/', payment_callback, name='payment_callback'),
]